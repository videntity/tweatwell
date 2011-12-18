from django.contrib import admin
from models import Freggie, Comment, NonVeg
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'

class FreggieAdmin(AdminImageMixin, admin.ModelAdmin):
    pass

admin.site.register(Freggie, FreggieAdmin)
admin.site.register(Comment)
admin.site.register(NonVeg)