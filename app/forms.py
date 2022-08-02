from django import forms

class PersonalInformation(forms.Form):
    drive_link = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Goggle Drive Link'}))
    