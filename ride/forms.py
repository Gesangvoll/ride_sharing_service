from django import forms
from django.forms import ModelForm
from .models import OwnerRequest, SharerRequest, Vehicle
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import DateTimeField


class RequestOwnerForm(ModelForm):


    class Meta:
        model = OwnerRequest
        fields = [
            'is_sharable',
            'destination',
            'vehicle_type',
            'passenger_num',
            'arrival_time',
            'special_vehicle_info'
        ]

        labels = {
            'is_sharable': 'Do you accept sharers?',
            'destination': 'Enter your destination',
            'passenger_num': 'How many passengers do you have?',
            'vehicle_type': 'What is your choice of vehicle type?',
            'arrival_time': 'What is your expected arrival time?',
            'special_vehicle_info' : 'What is your special vehicle demand?',

        }

# class RequestSharerForm(ModelForm):
#
#     class Meta:
#         model = SharerRequest
#         fields = [
#             ''
#         ]


class DriverRegistrationForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'plate_number',
            'type',
            'volume',
            'special_vehicle_info',
        ]

        labels = {
            'plate_number': 'What is your plate number?',
            'type': 'What is your vehicle type?',
            'volume': 'What is your vehicle volume',
            'special_vehicle_info': 'Do you have some special info?',
        }


