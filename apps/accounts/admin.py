from django.contrib import admin
from models import UserProfile, Permission, ValidPasswordResetKey, \
                    ValidSignupKey


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','twitter', 'dean_fruit_badge',
                    'dean_veggie_badge', 'joker_badge',
                    'president_badge')
    search_fields = ['user__email', 'twitter']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Permission)
admin.site.register(ValidPasswordResetKey)
admin.site.register(ValidSignupKey)