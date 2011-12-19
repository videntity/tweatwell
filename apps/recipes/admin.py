from django.contrib import admin
from models import Recipe, RecipeComment

admin.site.register(RecipeComment)

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Recipe, RecipeAdmin)