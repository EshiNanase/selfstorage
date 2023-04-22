from django import forms
from django.contrib.auth.forms import UserCreationForm
from personal_account.models import Client


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
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'E-mail'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'Телефон'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': ''
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

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': True, 'name': 'PASSWORD_EDIT1', 'id': 'PASSWORD1', 'value': 'abracadabra'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': True, 'name': 'PASSWORD_EDIT2', 'id': 'PASSWORD2', 'value': 'abracadabra'})
    )

    class Meta:
        model = Client
        fields = ['email', 'phone_number', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': True, 'name': 'EMAIL_EDIT', 'id': 'EMAIL'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control fs_24 ps-2 SelfStorage__input', 'disabled': True, 'name': 'PHONE_EDIT', 'id': 'PHONE'})
        }
        labels = {
            'email': 'E-mail',
            'phone_number': 'Телефон'
        }

