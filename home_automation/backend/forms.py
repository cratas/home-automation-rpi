from django import forms

from .models import Device

class ExportForm(forms.Form):
    something = forms.CharField(label='Your name')
    city = forms.ChoiceField(choices=[
    (choice.pk, choice) for choice in Device.objects.all()])
