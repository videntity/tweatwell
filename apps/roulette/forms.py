from django import forms
from models import Roulette
from ..accounts.models import UserProfile

class RouletteSpinForm(forms.ModelForm):
    class Meta:
        model = Roulette
        fields = ('points', )
        
class RouletteJokerForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('joker_badge', )