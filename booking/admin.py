from django.contrib import admin
from .models import Booking,ReviewRating,Complaints,Feedback


admin.site.register(Booking)
admin.site.register(ReviewRating)
admin.site.register(Complaints)
admin.site.register(Feedback)