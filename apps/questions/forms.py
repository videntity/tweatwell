from django import forms
from models import Answer, Question
def quiz_form_factory(question):

    properties = {
        'question' : forms.IntegerField(widget=forms.HiddenInput, \
            initial=question.id),
        'answers' : forms.ModelChoiceField(queryset= \
            question.answer_set)
    }

    return type('QuizForm', (forms.Form,), properties)