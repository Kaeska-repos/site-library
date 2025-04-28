from datetime import date
from django import forms

class Calendar(forms.DateInput):
    '''Calendar for choosing dates of birth.'''
    DATE_INPUT_WIDGET_REQUIRED_FORMAT = '%Y-%m-%d'

    def __init__(self, attrs={}, format=None):
        attrs.update({
            'class': 'form-control',
            'type': 'date',
            'max': date.today(),
        })
        self.format = format or self.DATE_INPUT_WIDGET_REQUIRED_FORMAT
        super().__init__(attrs, format=self.format)