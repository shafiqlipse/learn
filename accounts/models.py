from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_trainee = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    # is_accounts = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="profile/", blank=True, null=True)



class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive",
    )

    def __str__(self):
        return self.name

