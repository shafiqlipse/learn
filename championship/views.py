from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages
from xhtml2pdf import pisa
from io import BytesIO
from .models import *
from .forms import *
from django.db import IntegrityError
from django.core.files.base import ContentFile
import base64

from django.http import JsonResponse



# def get_venues(request):
#     season_id = request.GET.get("season_id")  # Get the selected season ID from the request
#     if season_id:
#         try:
#             season = Season.objects.get(id=season_id)  # Retrieve the season instance
#             venues = season.venue_set.values(
#                 "id", "name"
#             )  # Get related venues
#             return JsonResponse(list(venues), safe=False)
#         except Season.DoesNotExist:
#             return JsonResponse({"error": "Season not found"}, status=404)
#     return JsonResponse([], safe=False)

# def get_courses(request):
#     venue_id = request.GET.get("venue_id")  # Get the selected venue ID from the request
#     if venue_id:
#         try:
#             venue = CVenue.objects.get(id=venue_id)  # Retrieve the venue instance
#             courses = venue.course_set.values(
#                 "id", "name"
#             )  # Get related courses
#             return JsonResponse(list(courses), safe=False)
#         except CVenue.DoesNotExist:
#             return JsonResponse({"error": "COurse not found"}, status=404)
#     return JsonResponse([], safe=False)

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


def champie_add(request):
    if request.method == "POST":
        form = ChampiesForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                new_champie = form.save(commit=False)

                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_champie.photo = data  # Assign cropped image
                    except (ValueError, TypeError):
                        messages.error(request, "Invalid image data.")
                        return render(request, "champies/champie_new.html", {"form": form})

                new_champie.save()
                messages.success(
                    request,
                    "Registered successfully! PAY TO SECURE YOUR PLACE",
                )
                return redirect("addchampie")

            except IntegrityError:
                messages.error(request, "There was an error saving the champie.")
                return render(request, "champies/champie_new.html", {"form": form})

    else:
        form = ChampiesForm()

    context = {"form": form}
    return render(request, "champies/champie_new.html", context)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.decorators import login_required

from .filters import ChampieFilter  # Assume you have created this filter


@login_required(login_url="login")
def champies(request):
    # Get all champies
    champies = Champie.objects.all().order_by("-entry_date")

    # Apply the filter
    champie_filter = ChampieFilter(request.GET, queryset=champies)
    allchampies = champie_filter.qs

    if request.method == "POST":
        # Check which form was submitted
        if "Accreditation" in request.POST:
            template = get_template("champies/acrred.html")
            filename = "Champie_Accreditation.pdf"
        elif "Certificate" in request.POST:
            template = get_template(
                "champies/certficate_temaplate.html"
            )  # Your certificate template
            filename = "Champie_Certificate.pdf"
        else:
            return HttpResponse("Invalid form submission")

        # Generate PDF
        context = {"allchampies": allchampies}
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
            "champies/champies.html",
            {"champie_filter": champie_filter},
        )


def champie_details(request, id):
    champie = Champie.objects.get(id=id)

    context = {"champie": champie}
    return render(request, "champies/champie.html", context)


def champie_update(request, id):
    champie = get_object_or_404(Champie, id=id)

    if request.method == "POST":
        form = ChampiesForm(request.POST, request.FILES, instance=champie)
        if form.is_valid():
            try:
                new_champie = form.save(commit=False)

                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_champie.photo = data  # Assign cropped image
                    except (ValueError, TypeError):
                        messages.error(request, "Invalid image data.")
                        return render(request, "champies/champie_new.html", {"form": form})

                new_champie.save()
                messages.success(
                    request,
                    "Updated successfully! ",
                )
                return redirect("champies")

            except IntegrityError:
                messages.error(request, "There was an error saving the champie.")
                return render(request, "champies/champie_new.html", {"form": form})

    else:
        form = ChampiesForm(instance=champie)

    context = {
        "form": form,
        "champie": champie,
    }
    return render(request, "champies/update_champie.html", context)


def champie_delete(request, id):
    stud = Champie.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("champies")

    return render(request, "champies/delete_champie.html", {"obj": stud})


import csv
from django.http import HttpResponse


def export_csv(request):
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
    for obj in Champie.objects.all():
        writer.writerow(
            [
                obj.id,
                obj.first_name,
                obj.last_name,
                obj.place,
                obj.contact,
                obj.venue,
                obj.course,
                obj.level,
            ]
        )  # Replace with your model's fields

    return response



def activate_champie(request, id):
    champie = get_object_or_404(Champie, id=id)
    champie.status = "Active"
    champie.save()
    messages.success(request, "Champie activated successfully.")
    return redirect("champies") 
