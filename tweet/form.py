from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture',
            'cover_image',
            'bio',
            'location',
            'website',
        ]

        widgets = {
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Tell us about yourself'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Location'
                }
            ),

            'website': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://example.com'
                }
            ),

            'profile_picture': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'cover_image': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }