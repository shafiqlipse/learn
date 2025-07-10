from django.db import models


# Create your models here.


class Comiser(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to="b2_photos/",
    )
    comittee = models.CharField(max_length=15)
    role = models.CharField(max_length=125)


    def __str__(self):
        return self.first_name
