from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django import forms
from django.contrib import admin

User = get_user_model()

class MyUserCreationForm(UserCreationForm):
    #group = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'groups']


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['phone']