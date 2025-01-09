from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

from .views import *


urlpatterns = [
    # venues
    path("addxtrainee/", xtrainee_add, name="addxtrainee"),
    # path("teccred/", teccreditation, name="teccred"),
    path('export-xcsv/', export_xcsv, name='export_xcsv'),
    path("xtrainees/", xtrainees, name="xtrainees"),
    path("xtrainee/<int:id>", xtrainee_details, name="xtrainee"),
    path("delete_xtrainee/<int:id>", xtrainee_delete, name="delete_xtrainee"),
    path("update_xtrainee/<int:id>", xtrainee_update, name="update_xtrainee"),
    path("activate_xtrainee/<int:id>", activate_xtrainee, name="activate_xtrainee"),
    # path("process-payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
