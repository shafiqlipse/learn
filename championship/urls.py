from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

from .views import *


urlpatterns = [
    # venues
    path("addchampie/", champie_add, name="addchampie"),
    # path("teccred/", teccreditation, name="teccred"),
    path('export-csv/', export_csv, name='export_csv'),
    path("champies/", champies, name="champies"),
    path('get-courses/', get_courses, name='get_courses'),
    path('get-venues/', get_venues, name='get_venues'),
    path('get-level/', get_level, name='get_levels'),
    path("champie/<int:id>", champie_details, name="champie"),
    path("delete_champie/<int:id>", champie_delete, name="delete_champie"),
    path("update_champie/<int:id>", champie_update, name="update_champie"),
    path("activate_champie/<int:id>", activate_champie, name="activate_champie"),
    # path("process-payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
