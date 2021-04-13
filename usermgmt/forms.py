import usermgmt
from django import forms
from django.contrib.auth.models import User
from usermgmt.models import UserProfile
import datetime

class Adduser(forms.Form):
    """ """
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)
    expirydate = forms.DateField(initial=datetime.date.today) 

class Usermod(forms.Form):
    """ """
    username = forms.CharField(max_length=128)
    new_expirydate = forms.DateField(initial=datetime.date.today)

class Userdel(forms.Form):
    """ """
    username = forms.CharField(max_length=128)

class UserGrantAccess(forms.Form):
    """ """
    username = forms.CharField(max_length=128)

class UserForm(forms.ModelForm):
    """ """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    """ """
    class Meta:
        model = UserProfile
        fields = ('website',)

