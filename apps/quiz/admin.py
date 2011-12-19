from django.contrib import admin
from models import Question, Quiz, Response, Category, Answer

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz)
admin.site.register(Response)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Answer)