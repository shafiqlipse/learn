from django.contrib import admin
from accounts.models import *
from .models import *
from training.models import *
# from xcom.models import *
# from championship.models import *


class TraineeAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    list_display = ("first_name", "last_name", "season", "venue", "course", "level", "place")
    search_fields = ("first_name", "last_name", "venue", "course", "level")
    list_filter = ( "venue", "course", "level")
# # Register your models here.
admin.site.register(Trainee, TraineeAdmin) 
admin.site.register(User)
# admin.site.register(XTrainee)
admin.site.register(Season)
admin.site.register(Course)
# admin.site.register(XCourse)
admin.site.register(Venue)
# admin.site.register(XVenue)
admin.site.register(Level)
admin.site.register(District)
# admin.site.register(Championship)
# admin.site.register(Champie)
# admin.site.register(CVenue)
# # admin.site.register(Classroom)
# # admin.site.register(TOfficer)
# # admin.site.register(school_official)
