import usermgmt
from django import forms
from django.contrib.auth.models import User
from usermgmt.models import UserProfile

class Adduser(forms.Form):
    """ """
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)
    shelltype = forms.CharField(max_length=128)


class Usermod(forms.Form):
    """ """
    old_username = forms.CharField(max_length=128)
    new_username = forms.CharField(max_length=128)

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

class TestForm(forms.ModelForm):
    """ """
    address = forms.CharFiled(max_length=128)
