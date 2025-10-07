from django.db import models
from dashboard.models import District

class XVenue(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class XCourse(models.Model):
    name = models.CharField(max_length=50)
    venue = models.ManyToManyField(XVenue)

    def __str__(self):
        return self.name
    




class XTrainee(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True, blank=True)
   
    district = models.ForeignKey(District, on_delete=models.CASCADE,)
    venue = models.ForeignKey(XVenue, on_delete=models.CASCADE,)
    course = models.ForeignKey(XCourse, on_delete=models.CASCADE,)
    date_of_birth = models.DateField()
    entry_date = models.DateField(auto_now_add=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
    )

    photo = models.ImageField(upload_to="xtrainee_photos/")
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive",
    )

    is_paid = models.BooleanField(default=False)
    # is_trainee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
