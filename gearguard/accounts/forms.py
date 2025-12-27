from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import UserProfile


class StyledUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-300'
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' ' + css).strip()
            field.widget.attrs['placeholder'] = field.label
        
    # add extra fields not on User model
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=False)
    avatar = forms.ImageField(required=False)

    def save(self, commit=True):
        """
        Save the user and create/update their profile with form data.
        
        Args:
            commit (bool): Whether to save to database immediately
            
        Returns:
            User: The created user instance
            
        Raises:
            ValidationError: If profile creation/update fails
        """
        user = super().save(commit=commit)
        
        if not commit:
            return user
            
        try:
            with transaction.atomic():
                profile = self._get_or_create_profile(user)
                self._update_profile_fields(profile)
                profile.save()
        except Exception as e:
            # Clean up user if profile creation fails
            if user.pk:
                user.delete()
            raise ValidationError(f"Failed to create user profile: {str(e)}")
            
        return user
    
    def _get_or_create_profile(self, user):
        """
        Get existing profile or create a new one for the user.
        
        Args:
            user: The user instance
            
        Returns:
            UserProfile: The user's profile instance
        """
        try:
            return user.userprofile
        except UserProfile.DoesNotExist:
            return UserProfile(user=user)
    
    def _update_profile_fields(self, profile):
        """
        Update profile fields with cleaned form data.
        
        Args:
            profile: The UserProfile instance to update
        """
        # Get cleaned data once to avoid multiple dictionary lookups
        cleaned_data = self.cleaned_data
        
        # Update role if provided and valid
        role = cleaned_data.get('role')
        if role and role.strip():
            profile.role = role.strip()
        
        # Update avatar if provided
        avatar = cleaned_data.get('avatar')
        if avatar:
            profile.avatar = avatar
        
        # Update full_name if provided and profile doesn't have one
        username = cleaned_data.get('username')
        if username and username.strip() and not profile.full_name:
            profile.full_name = username.strip()
