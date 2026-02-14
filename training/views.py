from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages
from io import BytesIO
from .models import *
from .forms import *
from django.db import IntegrityError
from django.core.files.base import ContentFile
import base64
from django.contrib.auth.decorators import login_required
from .filters import TraineeFilter 
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import random
from django.db import transaction
from django.db import transaction as db_transaction
from django.conf import settings
import requests
import re
from django.urls import reverse
from django.http import JsonResponse
logger = logging.getLogger(__name__)

airtel_logger = logging.getLogger('airtel_callback')  # Use the specific logger

def get_venues(request):
    season_id = request.GET.get("season_id")  # Get the selected season ID from the request
    if season_id:
        try:
            season = Season.objects.get(id=season_id)  # Retrieve the season instance
            venues = season.venue_set.values(
                "id", "name"
            )  # Get related venues
            return JsonResponse(list(venues), safe=False)
        except Season.DoesNotExist:
            return JsonResponse({"error": "Season not found"}, status=404)
    return JsonResponse([], safe=False)

def get_courses(request):
    venue_id = request.GET.get("venue_id")  # Get the selected venue ID from the request
    if venue_id:
        try:
            venue = Venue.objects.get(id=venue_id)  # Retrieve the venue instance
            courses = venue.courses.values("id", "name")
  # Get related courses
            return JsonResponse(list(courses), safe=False)
        except Venue.DoesNotExist:
            return JsonResponse({"error": "COurse not found"}, status=404)
    return JsonResponse([], safe=False)

def get_levels(request):
    course_id = request.GET.get("course_id")  # Get the selected course ID from the request
    if course_id:
        try:
            course = Course.objects.get(id=course_id)  # Retrieve the course instance
            levels = course.level.values("id", "name")
  # Get related levels
            return JsonResponse(list(levels), safe=False)
        except Course.DoesNotExist:
            return JsonResponse({"error": "Level not found"}, status=404)
    return JsonResponse([], safe=False)


# def get_level(request):
#     course_id = request.GET.get("course_id")  # Get the selected course ID from the request
#     if course_id:
#         try:
#             courses = Course.objects.get(id=course_id)  # Retrieve the course instance
#             levels = courses.level_set.values(
#                 "id", "name"
#             )  # Get related disciplines
#             return JsonResponse(list(levels), safe=False)
#         except Venue.DoesNotExist:
#             return JsonResponse({"error": "Level not found"}, status=404)
#     return JsonResponse([], safe=False)

def trainee_add(request):
    if request.method == 'POST':
        form = TraineesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_trainee = form.save(commit=False)

                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_trainee.photo = data  # Assign cropped image
                    except (ValueError, TypeError):
                        messages.error(request, "Invalid image data.")
                        return render(request, "trainees/add_trainee.html", {"form": form})

                new_trainee.save()
                messages.success(
                    request,
                    "Trainee added successfully! Please proceed to payment.",
                )
                return redirect("addtrainee")

            except IntegrityError:
                messages.error(request, "There was an error saving the trainee.")
                return render(request, "trainees/add_trainee.html", {"form": form})

    else:
        form = TraineesForm()

    return render(request, 'trainees/add_trainee.html', {'form': form, 'amount': 10500 })  # Pass the amount to the template

def get_airtel_token():
    """
    Retrieve Airtel Money OAuth token.
    """
    try:
        url = "https://openapi.airtel.africa/auth/oauth2/token"
        headers = {"Content-Type": "application/json", "Accept": "*/*" }
        payload = {
            "client_id": settings.AIRTEL_MONEY_CLIENT_ID,
            "client_secret": settings.AIRTEL_MONEY_CLIENT_SECRET,
            "grant_type": "client_credentials",
        }

        response = requests.post(url, json=payload, headers=headers, params={})
        logger.info(f"Token Response: {response.status_code}, {response.text}")
        print(response.json())
        if response.status_code == 200:
            return response.json().get("access_token")

        # Handle common errors
        error_response = response.json()
        error_message = error_response.get("error_description", error_response.get("message", "Unknown error"))

        if response.status_code == 400:
            logger.error("Invalid request format. Check parameters.")
            return None
        elif response.status_code == 401:
            logger.error("Authentication failed. Check your API credentials.")
            return None
        elif response.status_code == 403:
            logger.error("Permission denied. Your account may not have access.")
            return None
        elif response.status_code == 500:
            logger.error("Airtel Money server error. Try again later.")
            return None

        logger.error(f"Failed to get token: {error_message}")
        return None

    except requests.exceptions.ConnectionError:
        logger.error("Network error: Unable to reach Airtel Money API.")
        return None
    except requests.exceptions.Timeout:
        logger.error("Request timed out: Airtel Money API took too long to respond.")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Unexpected request error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unknown error: {str(e)}")
        return None


@csrf_exempt
def airtel_payment_callback(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed", status=405)

    try:
        # Log raw request body
        raw_body = request.body.decode('utf-8')
        airtel_logger.info(f"🔔 Airtel Callback Received: {raw_body}")

        # Parse JSON payload
        payload = json.loads(raw_body)
        airtel_logger.info(f"📜 Parsed JSON Payload:\n{json.dumps(payload, indent=2)}")

        # Extract transaction details
        transaction = payload.get("transaction", {})
        transaction_id = transaction.get("id")
        status_code = transaction.get("status_code")
        airtel_money_id = transaction.get("airtel_money_id")
        
        
        # Find the Trainee record using transaction_id
        trainee = get_object_or_404(Trainee, transaction_id=transaction_id)

        # Map Airtel status to our system status
        status_mapping = {
            "TS": "COMPLETED",  # Transaction Successful
            "TF": "FAILED",      # Transaction Failed
            "TP": "PENDING",     # Transaction Pending
        }

        # Update payment status
        new_status = status_mapping.get(status_code, "Failed")

        with transaction.atomic():
            trainee.payment_status = new_status

            if new_status == "Completed":
                trainee.is_paid = True  # ✅ Mark as paid
                airtel_logger.info(f"✅ Payment successful for {trainee.first_name} {trainee.last_name}")
            else:
                trainee.is_paid = False
                airtel_logger.warning(f"⚠️ Payment not completed: {new_status} for {trainee.transaction_id}")

            trainee.save()

        airtel_logger.info(f"📌 Transaction ID: {transaction_id}, Status Code: {status_code}, Airtel Money ID: {airtel_money_id}")

        return JsonResponse({"message": "Callback received successfully"}, status=200)

    except json.JSONDecodeError:
        airtel_logger.error("❌ Invalid JSON received in callback")
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        airtel_logger.error(f"❌ Error processing callback: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
    
  
# def generate_unique_transaction_id():
#     """Generate a unique 12-digit transaction ID."""
#     while True:
#         transaction_id = str(random.randint(10**11, 10**12 - 1))  # 12-digit random number
#         if not Trainee.objects.filter(transaction_id=transaction_id).exists():  # Ensure uniqueness
#             return transaction_id


# def initiate_payment(request, id):
#     payment = get_object_or_404(Trainee, id=id)
    
#     try:
#         token = get_airtel_token()  
#         if not token:
#             return JsonResponse({"error": "Failed to get authentication token"}, status=500)

#         payment_url = "https://openapi.airtel.africa/merchant/v2/payments/"
#         transaction_id = generate_unique_transaction_id()  


#         headers = {
#             "Accept": "*/*",
#             "Content-Type": "application/json",
#             "X-Country": "UG",
#             "X-Currency": "UGX",
#             "Authorization": f"Bearer {token}",
#             "x-signature": settings.AIRTEL_API_SIGNATURE,  # Ensure this is set in settings.py
#             "x-key": settings.AIRTEL_API_KEY,  # Ensure this is set in settings.py
#         }

#         payload = {
#             "reference": str(payment.transaction_id),  # Use the Trainee ID as the reference
#             "subscriber": {
#                 "country": "UG",
#                 "currency": "UGX",
#                 "msisdn": re.sub(r"\D", "", str(payment.phone_number)).lstrip('0'),   # Remove non-numeric characters
#             },
#             "transaction": {
#                 "amount": float(payment.amount),  # Convert DecimalField to float
#                 "country": "UG",
#                 "currency": "UGX",
#                 "id": transaction_id,  # Use the generated transaction ID
#             }
#         }

#         response = requests.post(payment_url, json=payload, headers=headers)
#         logger.info(f"Trainee Response: {response.status_code}, {response.text}")

#        # Update payment record with transaction ID and set status to PENDING
#         with db_transaction.atomic():
#             payment.transaction_id = transaction_id
#             payment.status = "PENDING"  # Set status to pending until confirmed
#             payment.save()

#         if response.status_code == 200:
#             return redirect(reverse('payment_success', args=[payment.transaction_id]))  # ✅ Redirect to success page
#         else:
#             return JsonResponse({"error": "Failed to initiate payment", "details": response.text}, status=400)

#     except Exception as e:
#         logger.error(f"Trainee error: {str(e)}")
#         return JsonResponse({"error": str(e)}, status=500)


  

    
    
    
def payment_success(request, transaction_id):
    payment = Trainee.objects.filter(transaction_id=transaction_id).first()
    
    if not payment:
        return render(request, 'payment_failed.html', {'error': 'Transaction not found'})

    return render(request, 'emails/payment_success.html', {
        'amount': payment.amount,
        'transaction_id': payment.transaction_id,
        'timestamp': payment.created_at,  # Make sure your Trainee model has `created_at`
    })
    

 # Assume you have created this filter


@login_required(login_url="login")
def trainees(request):
    # Get all trainees
    trainees = Trainee.objects.all().order_by("-created_at")

    # Apply the filter
    trainee_filter = TraineeFilter(request.GET, queryset=trainees)
    alltrainees = trainee_filter.qs

    if request.method == "POST":
        # Check which form was submitted
        if "Accreditation" in request.POST:
            template = get_template("acrred.html")
            filename = "Trainee_Accreditation.pdf"
        elif "Certificate" in request.POST:
            template = get_template(
                "certficate_temaplate.html"
            )  # Your certificate template
            filename = "Trainee_Certificate.pdf"
        else:
            return HttpResponse("Invalid form submission")

        # Generate PDF
        context = {"alltrainees": alltrainees}
        html = template.render(context)

        # Create a PDF
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")

        pdf_buffer.seek(0)

        # Return the PDF as a response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.write(pdf_buffer.getvalue())
        return response
    else:
        # Render the filter form
        return render(
            request,
            "trainees/trainees.html",
            {"trainee_filter": trainee_filter},
        )


def trainee_details(request, id):
    trainee = Trainee.objects.get(id=id)

    context = {"trainee": trainee}
    return render(request, "trainees/trainee.html", context)


def trainee_update(request, id):
    trainee = get_object_or_404(Trainee, id=id)

    if request.method == "POST":
        form = TraineesForm(request.POST, request.FILES, instance=trainee)
        if form.is_valid():
            try:
                new_trainee = form.save(commit=False)

                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_trainee.photo = data  # Assign cropped image
                    except (ValueError, TypeError):
                        messages.error(request, "Invalid image data.")
                        return render(request, "trainee_new.html", {"form": form})

                new_trainee.save()
                messages.success(
                    request,
                    "Updated successfully! ",
                )
                return redirect("trainees")

            except IntegrityError:
                messages.error(request, "There was an error saving the trainee.")
                return render(request, "trainee_new.html", {"form": form})

    else:
        form = TraineesForm(instance=trainee)

    context = {
        "form": form,
        "trainee": trainee,
    }
    return render(request, "trainees/update_trainee.html", context)


def trainee_delete(request, id):
    stud = Trainee.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("trainees")

    return render(request, "trainees/delete_trainee.html", {"obj": stud})


import csv
from django.http import HttpResponse


def export_tcsv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="data.csv"'

    # Create a CSV writer object using the HttpResponse as the file.
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(
        [
            "id",
            "first_name",
            "last_name",
            "place",
            "contract",
            "district",
            "venue",
            "course",
            "level",
        ]
    )  # Replace with your model's fields

    # Write data rows
    for obj in Trainee.objects.all():
        writer.writerow(
            [
                obj.id,
                obj.first_name,
                obj.last_name,
                obj.place,
                obj.contact,
                obj.district,
                obj.venue,
                obj.course,
                obj.level,
            ]
        )  # Replace with your model's fields

    return response



def activate_trainee(request, id):
    trainee = get_object_or_404(Trainee, id=id)
    trainee.status = "Active"
    trainee.save()
    messages.success(request, "Trainee activated successfully.")
    return redirect("trainees") 


def archived_trainees(request):
    archived_trainees = Trainee.objects.filter(venue__status="Inactive").order_by("-created_at")
    trainee_filter = TraineeFilter(request.GET, queryset=archived_trainees)
    archived_trainees = trainee_filter.qs

    return render(
        request,
        "trainees/archived_trainees.html",
        {"trainee_filter": trainee_filter, "archived_trainees": archived_trainees},
    )

def unpaid_trainees(request):
    unpaid_trainees = Trainee.objects.filter(venue__status="Active",payment_status="Pending").order_by("-created_at")
    trainee_filter = TraineeFilter(request.GET, queryset=unpaid_trainees)
    unpaid_trainees = trainee_filter.qs

    return render(
        request,
        "trainees/archived_trainees.html",
        {"trainee_filter": trainee_filter, "unpaid_trainees": unpaid_trainees},
    )