from django.db import models
from dashboard.models import District
from training.models import Course, Level
# Create your models here.


class Championship(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    year = models.IntegerField()
    status = models.CharField( choices=[("Active", "Active"), ("Inactive", "Inactive")], max_length=10, default="Active" ,null=True, blank=True)

    def __str__(self):
        return self.name


class CVenue(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ManyToManyField(Championship, related_name='venues', blank=True)
    def __str__(self):
        return self.name




class Champie(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE,null=True,blank=True)
    venue = models.ForeignKey(CVenue, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    entry_date = models.DateField(auto_now_add=True)
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
    photo = models.ImageField(upload_to="champie_photos/")
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive",
    )
    is_paid = models.BooleanField(default=False)
    # is_champie = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
