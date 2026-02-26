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


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO




def comiser_add(request):
    if request.method == "POST":
        form = ComisersForm(request.POST, request.FILES)
        
        if form.is_valid():
            comiser = form.save()
            messages.success(request, f'Comiser "{comiser.first_name}" added successfully!')
            return redirect('addcomiser')  # Redirect to list or detail view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ComisersForm()
    
    context = {
        "form": form,
        "title": "Add New Comiser"
    }
    return render(request, "comiser/comiser_new.html", context)


def generate_accreditation_pdf(request):
    comisers = Comiser.objects.all()

    # Load the template
    template = get_template("comiser/acred.html")
    context = {
        "comisers": comisers,
         # in case you need it for images
    }

    html = template.render(context)
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    if pisa_status.err:
        return HttpResponse("Error generating PDF <pre>" + html + "</pre>")

    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Comiser_Accreditation.pdf"'
    return response

def comisers(request):
    # Get all comisers
    comisers = Comiser.objects.all()

    return render(request, "comiser/comisers.html", {"comisers": comisers})


def comiser_details(request, id):
    comiser = Comiser.objects.get(id=id)

    context = {"comiser": comiser}
    return render(request, "comiser/comiser.html", context)


def comiser_update(request, id):
    comiser = get_object_or_404(Comiser, id=id)

    if request.method == "POST":
        form = ComisersForm(request.POST, request.FILES, instance=comiser)
        if form.is_valid():
            form.save()
            messages.success(request, "Comisers information updated successfully!")
            return redirect("comiser", id=comiser.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ComisersForm(instance=comiser)

    context = {
        "form": form,
        "comiser": comiser,
    }
    return render(request, "comiser/update_comiser.html", context)


def comiser_delete(request, id):
    stud = Comiser.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("comisers")

    return render(request, "comiser/delete_comiser.html", {"obj": stud})

