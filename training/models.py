from django.db import models
from accounts.models import *
from dashboard.models import *

# Create your models here.

class Trainee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,related_name=
                                 "trainee_district",)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
    )
    designation = models.CharField(
        max_length=20,
        choices=[
            ("Student", "Student"),
            ("Primary Teacher", "Primary Teacher"),
            ("Secondary Teacher", "Secondary Teacher"),
            ("Other", "Other"),
        ],
    )
    photo = models.ImageField(upload_to="trainee_photos/")
    residence_type = models.CharField(
        max_length=20,
        choices=[
            ("Residential", "Residential"),
            ("Non Residential", "Non Residential"),
        ],
    )
    

    # 💳 Payment-related fields

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



