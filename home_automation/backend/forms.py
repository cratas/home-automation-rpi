from django import forms
from .models import Device, PullDevice, PushDevice, Room, SmartDevice

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
    time_title = forms.CharField(required=False)
    datetime_title = forms.CharField(required=False)
    date_title = forms.CharField(required=False)
    datetime_format = forms.CharField(required=False)
    communication_counter = forms.IntegerField(required=False)

    class Meta:
        model = PushDevice
        fields = ['device_name', 'identifier', 'is_active', 'room', 'has_error', 'communication_interval','datetime_title', 'date_title', 'time_title', 'datetime_format']


class PullDeviceForm(forms.ModelForm):
    time_title = forms.CharField(required=False)
    datetime_title = forms.CharField(required=False)
    date_title = forms.CharField(required=False)
    datetime_format = forms.CharField(required=False)
    communication_counter = forms.IntegerField(required=False)
    delimiter = forms.CharField(required=False)

    class Meta:
        model = PullDevice
        fields = ['device_name', 'identifier', 'is_active', 'room'
                , 'source_address','source_type','format', 'delimiter', 'has_error','communication_interval', 'datetime_title', 'date_title', 'time_title','datetime_format']

class SmartDeviceForm(forms.ModelForm):
    class Meta:
        model = SmartDevice
        fields = ['identifier', 'device_name', 'type', 'room', 'is_active']