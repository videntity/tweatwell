from django.contrib import admin
from tweatwell.web.foodreport.models import FoodReport, UserStatusReport

admin.site.register(FoodReport)
admin.site.register(UserStatusReport)