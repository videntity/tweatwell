from django.contrib import admin
from models import UserProfile, Permission, ValidSMSCode, ValidPasswordResetKey


admin.site.register(UserProfile)
admin.site.register(Permission)
admin.site.register(ValidSMSCode)
admin.site.register(ValidPasswordResetKey)