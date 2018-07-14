from django.forms import ModelForm
from django import forms
from .models import *


class KolicinaForm(forms.Form):
    #CHOICES=[(25,25),
    #     (50,50),
    #     (100,100)]
    # zaenkrat tukaj brez staticnih vsebin
    #staticne_kolicine = forms.ChoiceField(label='',choices=CHOICES, widget=forms.RadioSelect())
    kolicina = forms.IntegerField(label='Količina')

