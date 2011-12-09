from django import forms
from models import QuestionAnswer

class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('answer',)