from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from dashboard.views import *
from accounts.views import *
from training.views import *
from trainers.views import *



urlpatterns = [
    path("admin/", admin.site.urls),
    # venues
    path("", user_login, name="login"),
    # venues
    path("dashboard/", include("dashboard.urls")),
    path("auth/", include("accounts.urls")),
    path("training/", include("training.urls")),
    path("xtraining/", include("xcom.urls")),
    path("trainers/", include("trainers.urls")),
    path("resources/", include("resources.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
