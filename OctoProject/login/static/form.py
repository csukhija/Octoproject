from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class LoginForm(forms.Form):
    username=forms.CharField(label=(u'user'))
    password=forms.CharField(label=(u'pass'))