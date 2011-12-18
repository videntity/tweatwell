from django import forms
from models import RecipeComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = RecipeComment
        fields = ('text',)