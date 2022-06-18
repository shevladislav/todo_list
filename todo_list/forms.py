from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Task


class RegistrationUserForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=25)
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('sign up', 'Sign up'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def clean_password_confirm(self):
        password_one = self.cleaned_data.get('password')
        password_two = self.cleaned_data.get('password_confirm')
        password_has_num = [True for sym in password_one if sym.isdigit()]

        if password_one != password_two:
            raise forms.ValidationError('Passwords do not match')
        if len(password_one) < 8:
            raise forms.ValidationError('Password length must be greater than 8 characters')
        if not password_one[0].isalpha() and not password_one[0].isupper():
            raise forms.ValidationError('The first character must be a capital letter')
        if not sum(password_has_num) > 0:
            raise forms.ValidationError('Password must contain at least one number')

        return password_two

    def clean_email(self):
        email = self.cleaned_data.get('email')
        check_mail = User.objects.filter(email=email)

        if len(check_mail) > 0:
            raise forms.ValidationError('This email address is not available')

        return email


class LoginUserForm(forms.Form):
    username = forms.CharField(required=True, max_length=25)
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('log in', 'Log in'))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        check_username = User.objects.filter(username=username)

        if not len(check_username):
            raise forms.ValidationError('User with this username does not exist')

        check_password = authenticate(username=username, password=password)

        if check_password is None:
            raise forms.ValidationError('Invalid password')

        return self.cleaned_data


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ('title', 'body', 'deadline')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save'))



