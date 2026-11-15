from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя (логин)',
        widget=forms.TextInput(attrs={'placeholder': 'Придумайте логин'})
    )
    email = forms.EmailField(
        label='Электронная почта',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.ru'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите надежный пароль'
        
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'