from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *



urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("seasons/", seasons_view, name="seasons"),
    path("venues/", venues_view, name="venues"),
    path("courses/", courses_view, name="courses"),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
