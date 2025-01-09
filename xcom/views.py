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




def xtrainee_add(request):
    if request.method == "POST":
        form = XTraineesForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                new_xtrainee = form.save(commit=False)

                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_xtrainee.photo = data  # Assign cropped image
                    except (ValueError, TypeError):
                        messages.error(request, "Invalid image data.")
                        return render(request, "xtrainee_new.html", {"form": form})

                new_xtrainee.save()
                messages.success(
                    request,
                    "Registered successfully! PAY TO SECURE YOUR PLACE",
                )
                return redirect("addxtrainee")

            except IntegrityError:
                messages.error(request, "There was an error saving the xtrainee.")
                return render(request, "xtrainee_new.html", {"form": form})

    else:
        form = XTraineesForm()

    context = {"form": form}
    return render(request, "xtrainee_new.html", context)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.decorators import login_required

from .filters import XTraineeFilter  # Assume you have created this filter


@login_required(login_url="login")
def xtrainees(request):
    # Get all xtrainees
    xtrainees = XTrainee.objects.all().order_by("-entry_date")

    # Apply the filter
    xtrainee_filter = XTraineeFilter(request.GET, queryset=xtrainees)
    allxtrainees = xtrainee_filter.qs

    if request.method == "POST":
        # Check which form was submitted
        if "Accreditation" in request.POST:
            template = get_template("xacrred.html")
            filename = "XTrainee_Accreditation.pdf"
        elif "Certificate" in request.POST:
            template = get_template(
                "certficate_xtemaplate.html"
            )  # Your certificate template
            filename = "XTrainee_Certificate.pdf"
        else:
            return HttpResponse("Invalid form submission")

        # Generate PDF
        context = {"allxtrainees": allxtrainees}
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
            "xtrainees.html",
            {"xtrainee_filter": xtrainee_filter},
        )


def xtrainee_details(request, id):
    xtrainee = XTrainee.objects.get(id=id)

    context = {"xtrainee": xtrainee}
    return render(request, "xtrainee.html", context)


def xtrainee_update(request, id):
    xtrainee = get_object_or_404(XTrainee, id=id)

    if request.method == "POST":
        form = XTraineesForm(request.POST, request.FILES, instance=xtrainee)
        if form.is_valid():
            try:
                new_xtrainee = form.save(commit=False)

                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_xtrainee.photo = data  # Assign cropped image
                    except (ValueError, TypeError):
                        messages.error(request, "Invalid image data.")
                        return render(request, "xtrainee_new.html", {"form": form})

                new_xtrainee.save()
                messages.success(
                    request,
                    "Updated successfully! ",
                )
                return redirect("xtrainees")

            except IntegrityError:
                messages.error(request, "There was an error saving the xtrainee.")
                return render(request, "xtrainee_new.html", {"form": form})

    else:
        form = XTraineesForm(instance=xtrainee)

    context = {
        "form": form,
        "xtrainee": xtrainee,
    }
    return render(request, "update_xtrainee.html", context)


def xtrainee_delete(request, id):
    stud = XTrainee.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("xtrainees")

    return render(request, "delete_xtrainee.html", {"obj": stud})


import csv
from django.http import HttpResponse


def export_xcsv(request):
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
           
        ]
    )  # Replace with your model's fields

    # Write data rows
    for obj in XTrainee.objects.all():
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
           
            ]
        )  # Replace with your model's fields

    return response



def activate_xtrainee(request, id):
    xtrainee = get_object_or_404(XTrainee, id=id)
    xtrainee.status = "Active"
    xtrainee.save()
    messages.success(request, "XTrainee activated successfully.")
    return redirect("xtrainees") 
