from django import forms
from models import NonVeg

class NonVegForm(forms.ModelForm):
    class Meta:
        model = NonVeg
        fields = ('nonveg','quantity','text',)