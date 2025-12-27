"""
Custom password validators for enhanced security.
"""
import re
import logging
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class ComplexityPasswordValidator:
    """
    Validates that the password contains a mix of character types.
    Requires at least one uppercase, lowercase, digit, and special character.
    """
    
    def __init__(self, min_uppercase=1, min_lowercase=1, min_digits=1, min_special=1):
        # Validate initialization parameters
        if not all(isinstance(x, int) and x >= 0 for x in [min_uppercase, min_lowercase, min_digits, min_special]):
            raise ValueError("All minimum requirements must be non-negative integers")
        
        self.min_uppercase = min_uppercase
        self.min_lowercase = min_lowercase
        self.min_digits = min_digits
        self.min_special = min_special
    
    def validate(self, password, user=None):
        """Validate password complexity with comprehensive error handling."""
        if not isinstance(password, str):
            raise ValidationError(_('Password must be a string.'))
        
        if not password:
            raise ValidationError(_('Password cannot be empty.'))
        
        errors = []
        
        try:
            # Count character types with error handling
            uppercase_count = len(re.findall(r'[A-Z]', password))
            lowercase_count = len(re.findall(r'[a-z]', password))
            digit_count = len(re.findall(r'\d', password))
            special_count = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
        except re.error as e:
            logger.error(f"Regex error in password validation: {e}")
            raise ValidationError(_('Password contains invalid characters.'))
        except Exception as e:
            logger.error(f"Unexpected error in password validation: {e}")
            raise ValidationError(_('Password validation failed.'))
        
        # Check requirements
        if uppercase_count < self.min_uppercase:
            errors.append(
                _('Password must contain at least %(min)d uppercase letter(s).') % 
                {'min': self.min_uppercase}
            )
        
        if lowercase_count < self.min_lowercase:
            errors.append(
                _('Password must contain at least %(min)d lowercase letter(s).') % 
                {'min': self.min_lowercase}
            )
        
        if digit_count < self.min_digits:
            errors.append(
                _('Password must contain at least %(min)d digit(s).') % 
                {'min': self.min_digits}
            )
        
        if special_count < self.min_special:
            errors.append(
                _('Password must contain at least %(min)d special character(s).') % 
                {'min': self.min_special}
            )
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        """Return help text for this validator."""
        return _(
            'Your password must contain at least %(uppercase)d uppercase letter, '
            '%(lowercase)d lowercase letter, %(digits)d digit, and '
            '%(special)d special character (!@#$%%^&*(),.?":{}|<>).'
        ) % {
            'uppercase': self.min_uppercase,
            'lowercase': self.min_lowercase,
            'digits': self.min_digits,
            'special': self.min_special,
        }


class RepeatingCharacterValidator:
    """
    Validates that the password doesn't contain too many repeating characters.
    """
    
    def __init__(self, max_repeating=3):
        self.max_repeating = max_repeating
    
    def validate(self, password, user=None):
        """Check for repeating characters."""
        # Check for consecutive repeating characters
        for i in range(len(password) - self.max_repeating + 1):
            if len(set(password[i:i + self.max_repeating])) == 1:
                raise ValidationError(
                    _('Password cannot contain %(max)d or more consecutive identical characters.') % 
                    {'max': self.max_repeating}
                )
    
    def get_help_text(self):
        """Return help text for this validator."""
        return _(
            'Your password cannot contain %(max)d or more consecutive identical characters.'
        ) % {'max': self.max_repeating}


class SequentialCharacterValidator:
    """
    Validates that the password doesn't contain sequential characters.
    """
    
    def __init__(self, max_sequential=3):
        self.max_sequential = max_sequential
    
    def validate(self, password, user=None):
        """Check for sequential characters."""
        # Check for ascending sequences
        for i in range(len(password) - self.max_sequential + 1):
            sequence = password[i:i + self.max_sequential]
            if self._is_sequential(sequence):
                raise ValidationError(
                    _('Password cannot contain %(max)d or more sequential characters.') % 
                    {'max': self.max_sequential}
                )
    
    def _is_sequential(self, sequence):
        """Check if a sequence is sequential (ascending or descending)."""
        if len(sequence) < 2:
            return False
        
        # Convert to ASCII values
        ascii_values = [ord(char) for char in sequence]
        
        # Check ascending sequence
        ascending = all(
            ascii_values[i] + 1 == ascii_values[i + 1] 
            for i in range(len(ascii_values) - 1)
        )
        
        # Check descending sequence
        descending = all(
            ascii_values[i] - 1 == ascii_values[i + 1] 
            for i in range(len(ascii_values) - 1)
        )
        
        return ascending or descending
    
    def get_help_text(self):
        """Return help text for this validator."""
        return _(
            'Your password cannot contain %(max)d or more sequential characters (e.g., abc, 123).'
        ) % {'max': self.max_sequential}
