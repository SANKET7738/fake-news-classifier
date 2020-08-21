from django import forms

class InputForm(forms.Form):
    input_url = forms.URLField(label='',widget=forms.TextInput(attrs={'class':'form-control','type':'text','id':'news_link','placeholder':'Post your link'}))