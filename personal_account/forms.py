from django import forms
from django.contrib.auth.forms import UserCreationForm
from personal_account.models import CustomUser


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
        model = CustomUser
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'E-mail'}),
        }
        labels = {
            'email': ''
        }


class LoginUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'E-mail'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey', 'placeholder': 'Пароль'}),
        }
        labels = {
            'email': '',
            'password': ''
        }
