__author__ = 'Ronald'
from django.forms import TextInput, PasswordInput, Form, CharField
from apps.actores.forms import UserForm


class LoginForm(Form):
    print(UserForm.Meta.widgets['username'].attrs)
    username = CharField(max_length=30, widget=UserForm.Meta.widgets['username'])
    password = CharField(max_length=50, widget=UserForm.Meta.widgets['password'])
