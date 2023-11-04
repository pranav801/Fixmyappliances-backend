from django.contrib import admin
from .models import Booking,ReviewRating,Complaints


admin.site.register(Booking)
admin.site.register(ReviewRating)
admin.site.register(Complaints)