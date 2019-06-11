from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class OrderForm(forms.Form):
    Имя= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    Телефон = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Сообщение = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )