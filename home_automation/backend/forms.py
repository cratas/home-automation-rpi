from django import forms
from .widgets import DatePickerInput, TimePickerInput
from .models import Device, PullDevice, PushDevice, Room

class ExportForm(forms.Form):
    from_date = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'))
    to_date = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )

    device = forms.MultipleChoiceField(choices=[
    (choice.pk, choice) for choice in Device.objects.all()])


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']

class PushDeviceForm(forms.ModelForm):
    class Meta:
        model = PushDevice
        fields = ['device_name', 'identifier', 'is_active', 'room']


class PullDeviceForm(forms.ModelForm):
    class Meta:
        model = PullDevice
        fields = ['device_name', 'identifier', 'is_active', 'room'
                , 'source_address','source_type','format','has_error']