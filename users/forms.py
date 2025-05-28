# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() # Add an email field

    class Meta(UserCreationForm.Meta):
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields + ('email',) # Add email to the fields