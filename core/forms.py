from django import forms
from .models import Slider



class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'image', 'link', 'order']





