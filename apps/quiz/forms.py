#!/usr/bin/env python
from django import forms
from models import Quiz
from django.forms.util import ErrorList
import types


class TakeQuizForm(forms.Form):
    """A form containing a quiz made up of required and random questions"""
    
    def __init__(self, must_ask_questions, random_questions, answers, *args, **kwargs):
        """An overloaded init to take in q&a so we can dynamicly build form"""
        super(TakeQuizForm, self).__init__(*args, **kwargs)
        
        # now we add each must ask question individually
        for i, question in enumerate(must_ask_questions):
            choice_list=[]
            for j, answer in enumerate(answers):
                """pull the answer choices that match the question"""
                #print answer.question.id, question.id
                if (answer.question.id==question.id):
                    #print answer
                    choice_list.append((answer.answer,answer.answer))
            choice_tuple=tuple(choice_list)        
            self.fields[question.slug] = forms.ChoiceField(widget=forms.RadioSelect,
                                label=question.question_text,
                                choices=choice_tuple)
            
        choice_list=[]
        # now we add each random question individually
        for i, question in enumerate(random_questions):
            choice_list=[]
            for j, answer in enumerate(answers):
                """pull the answer choices that match the question"""
                #print answer.question.id, question.id
                if (answer.question.id==question.id):
                    choice_list.append((answer.answer,answer.answer))
            choice_tuple=tuple(choice_list)        
            self.fields[question.slug] = forms.ChoiceField(
                                        widget=forms.RadioSelect,
                                        label=question.question_text,
                                        choices=choice_tuple)

                
