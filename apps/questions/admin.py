from django.contrib import admin
from models import Answer, Question, CorrectAnswerPoints, CurrentQuestion


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CorrectAnswerPoints)
admin.site.register(CurrentQuestion)