from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, Class_rooms, Trainings, Training_days, Students, Date

#admin.site.register(get_user_model())
admin.site.register(User)
#admin.site.register(Seats)
admin.site.register(Class_rooms)
admin.site.register(Trainings)
admin.site.register(Training_days)
admin.site.register(Students)
admin.site.register(Date)


# Register your models here.
