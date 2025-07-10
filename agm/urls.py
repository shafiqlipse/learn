from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

from .views import *


urlpatterns = [
    # venues

    # path("process-
    # 
    # venues
    path("addcomiser/", comiser_add, name="addcomiser"),
    path("teccred/", generate_accreditation_pdf, name="teaccred"),
    path("comisers/", comisers, name="comisers"),
    path("comiser/<int:id>", comiser_details, name="comiser"),
    path("delete_comiser/<int:id>", comiser_delete, name="delete_comiser"),
    path("update_comiser/<int:id>", comiser_update, name="update_comiser"),
    # path("process-p
    # payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
