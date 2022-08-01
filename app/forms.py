from cProfile import label
from django import forms

current_location_choices=(
    ("1", "Bhubaneswar/Orissa"),
    ("2", "New Delhi/NCR"),
    ("3", "Benguluru"),
    ("4", "Kolkata"),
    ("5", "Pune"),
    ("6", "Mumbai"),
    ("7", "Others")
)
preferred_location_choices=(
    ("1", "Bhubaneswar"),
    ("2", "New Delhi/NCR"),
    ("3", "Remote Working"),
)

class PersonalInformation(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    dob = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Date Of Birth'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    linkedIn = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'LinkedIn Profile Link'}))
    skypeId = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Skype Id'}))
    drive_link = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Goggle Drive Link'}))
    