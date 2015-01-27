from django.contrib import admin
from models import Freggie, Comment, BadgePoints, FreggieGoal, NonVeg
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'

class FreggieAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ( 'user', 'freggie', 'evdt', 'photo')

admin.site.register(Freggie, FreggieAdmin)
admin.site.register(FreggieGoal)
admin.site.register(Comment)
admin.site.register(BadgePoints)
admin.site.register(NonVeg)