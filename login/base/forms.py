from django import forms
from .models import UserProfile, Report

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  
        fields = ['profile_picture']