from django import forms
from models import Roulette

class RouletteSpinForm(forms.ModelForm):
    class Meta:
        model = Roulette
        fields = ('points', )