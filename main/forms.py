from django import forms
from .models import Package, CustomUser
from django.db import models
from django.contrib.auth.forms import UserCreationForm


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'description', 'price', 'duration', 'image', 'expiry_date']


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[choice for choice in CustomUser.ROLE_CHOICES if choice[0].lower() != 'admin']
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        # Force regular user role
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()
        return user