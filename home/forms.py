from django import forms

from users.models import User
from api.models import ApiKey


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput)
