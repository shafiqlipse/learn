from django.db import models
from accounts.models import District

# Create your models here.


class Season(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    year = models.IntegerField()
    # status = models.CharField( choices=[("Active", "Active"), ("Inactive", "Inactive")], max_length=10, default="Active" ,null=True, blank=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ManyToManyField(Season)
    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ManyToManyField(Venue)

    def __str__(self):
        return self.name
    

    
class Level(models.Model):
    name = models.CharField(max_length=50)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Trainee(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True, blank=True)
    tid = models.CharField(max_length=50, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE,null=True,blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
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
    photo = models.ImageField(upload_to="trainee_photos/")
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive",
    )
    residence_type = models.CharField(
        max_length=20,
        choices=[
            ("Residential", "Residential"),
            ("Non Residential", "Non Residential"),
        ],
    )
    is_paid = models.BooleanField(default=False)
    # is_trainee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
