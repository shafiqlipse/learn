from django.db import models

from accounts.models import User




class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Season(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    year = models.IntegerField()
    status = models.CharField( choices=[("Active", "Active"), ("Inactive", "Inactive")], max_length=10, default="Active" ,null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=50)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', blank=True)
    status = models.CharField( choices=[("Active", "Active"), ("Inactive", "Inactive")], max_length=10, default="Active" ,null=True, blank=True)
    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    level = models.ManyToManyField('Level', null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    

    
class Level(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name