from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import *

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'user_type']
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'rows': 3}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your old password'
        })
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password'
        })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password'
        })
        

class LeasePropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['house_image', 'house_video', 'location', 'price', 'details', 'title', 'beds', 'bath', 'garage', 'area']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter house details'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter house title'}),
            'beds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of beds'}),
            'bath': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of baths'}),
            'garage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of garages'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter area in square meters or feet'}),
        }


class PropertySearchForm(forms.Form):
    beds = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Number of beds'}))
    bath = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Number of baths'}))
    area = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Minimum area (m²)', 'step': '0.001'})  # Allow 3 decimal places
    )
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Minimum price', 'step': '0.01'})  # Allow 2 decimal places
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Maximum price', 'step': '0.01'})  # Allow 2 decimal places
    )
    garage = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Number of garages'}))