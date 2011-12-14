from django.contrib import admin
from models import UserProfile, Permission, ValidPasswordResetKey, \
                    ValidSignupKey, Award


admin.site.register(UserProfile)
admin.site.register(Award)
admin.site.register(Permission)
admin.site.register(ValidPasswordResetKey)
admin.site.register(ValidSignupKey)