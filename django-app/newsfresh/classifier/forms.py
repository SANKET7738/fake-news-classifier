from django import forms

class InputForm(forms.Form):
    input_url = forms.URLField()