from django import forms
from models import Comment, Freggie, NonVeg

class FreggieForm(forms.ModelForm):
    class Meta:
        model = Freggie
        fields = ('freggie','freggie_other','quantity', 'text', 'photo' )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        
class NonVegForm(forms.ModelForm):
    class Meta:
        model = NonVeg
        fields = ('nonveg','text',)