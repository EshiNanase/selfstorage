from django import forms
from django.contrib.auth.forms import UserCreationForm
from personal_account.models import Client
from phonenumber_field.formfields import PhoneNumberField


class RegisterUserForm(UserCreationForm):

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'Подтверждение пароля'})
    )

    class Meta:
        model = Client
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'E-mail'}),
        }
        labels = {
            'email': ''
        }


class LoginUserForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'E-mail'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'Пароль'}),
        }
        labels = {
            'email': '',
            'password': ''
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['email', 'phone_number', 'password']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'readonly': True}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'readonly': True}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'readonly': True}),
        }
        labels = {
            'email': 'E-mail',
            'password': 'Пароль',
            'phone_number': 'Телефон'
        }

