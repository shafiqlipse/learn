from django.contrib import admin
from accounts.models import *
from training.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Trainee)
admin.site.register(Season)
admin.site.register(Course)
admin.site.register(Venue)
admin.site.register(Level)
admin.site.register(District)

# # admin.site.register(School)
# # admin.site.register(City)
# admin.site.register(Zone)
# # admin.site.register(Classroom)
# # admin.site.register(TOfficer)
# # admin.site.register(school_official)
