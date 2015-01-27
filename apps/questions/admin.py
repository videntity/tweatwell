from django.contrib import admin
from models import Answer, Question, CorrectAnswerPoints, CurrentQuestion



class AnswerAdmin(admin.ModelAdmin):
    list_display = ('test',  'question', 'is_correct')


admin.site.register(Question)
admin.site.register(Answer,AnswerAdmin )
admin.site.register(CorrectAnswerPoints)
admin.site.register(CurrentQuestion)