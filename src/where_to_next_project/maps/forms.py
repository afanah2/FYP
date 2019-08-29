from django import forms


class InputForm(forms.Form):
    CHOICES=[('Default', 'Use Default Settings'),
         ( 'Advanced', 'Advanced Settings')]

    Settings = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(
        attrs = {
            "class": "radio-inline"
        }
    ))

    number_of_drivers = forms.IntegerField(widget=forms.NumberInput(attrs={'size':'0'}), min_value=1, max_value = 100)

    cities = forms.CharField(widget = forms.HiddenInput())
