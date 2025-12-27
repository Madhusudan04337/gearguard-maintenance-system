"""
Password utility functions for enhanced security and performance.
"""
import hashlib
import secrets
import string
from typing import Optional, Dict, Any, List
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache


User = get_user_model()


class PasswordStrengthAnalyzer:
    """
    Analyzes password strength and provides feedback.
    """
    
    @staticmethod
    def calculate_strength_score(password: str) -> Dict[str, Any]:
        """
        Calculate password strength score (0-100).
        
        Args:
            password: The password to analyze
            
        Returns:
            Dict containing score and feedback
        """
        score = 0
        feedback = []
        
        # Length scoring
        length = len(password)
        if length >= 12:
            score += 25
        elif length >= 8:
            score += 15
            feedback.append("Consider using a longer password (12+ characters)")
        else:
            feedback.append("Password is too short (minimum 8 characters)")
        
        # Character variety scoring
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*(),.?\":{}|<>" for c in password)
        
        variety_score = sum([has_lower, has_upper, has_digit, has_special]) * 15
        score += variety_score
        
        if not has_lower:
            feedback.append("Add lowercase letters")
        if not has_upper:
            feedback.append("Add uppercase letters")
        if not has_digit:
            feedback.append("Add numbers")
        if not has_special:
            feedback.append("Add special characters")
        
        # Complexity bonus
        if length >= 16 and variety_score == 60:
            score += 10
            
        return {
            'score': min(score, 100),
            'strength': PasswordStrengthAnalyzer._get_strength_label(score),
            'feedback': feedback
        }
    
    @staticmethod
    def _get_strength_label(score: int) -> str:
        """Get strength label based on score."""
        if score >= 80:
            return "Very Strong"
        elif score >= 60:
            return "Strong"
        elif score >= 40:
            return "Moderate"
        elif score >= 20:
            return "Weak"
        else:
            return "Very Weak"


class PasswordGenerator:
    """
    Secure password generator with customizable options.
    """
    
    @staticmethod
    def generate_secure_password(
        length: int = 16,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_special: bool = True,
        exclude_ambiguous: bool = True
    ) -> str:
        """
        Generate a cryptographically secure password.
        
        Args:
            length: Password length
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_special: Include special characters
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, 1, etc.)
            
        Returns:
            Generated password string
        """
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")
        
        # Build character set
        chars = ""
        required_chars = []
        
        if include_lowercase:
            lowercase = string.ascii_lowercase
            if exclude_ambiguous:
                lowercase = lowercase.replace('l', '').replace('o', '')
            chars += lowercase
            required_chars.append(secrets.choice(lowercase))
        
        if include_uppercase:
            uppercase = string.ascii_uppercase
            if exclude_ambiguous:
                uppercase = uppercase.replace('I', '').replace('O', '')
            chars += uppercase
            required_chars.append(secrets.choice(uppercase))
        
        if include_digits:
            digits = string.digits
            if exclude_ambiguous:
                digits = digits.replace('0', '').replace('1', '')
            chars += digits
            required_chars.append(secrets.choice(digits))
        
        if include_special:
            special = "!@#$%^&*(),.?\":{}|<>"
            chars += special
            required_chars.append(secrets.choice(special))
        
        if not chars:
            raise ValueError("At least one character type must be included")
        
        # Generate password ensuring required characters are included
        password_chars = required_chars[:]
        remaining_length = length - len(required_chars)
        
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(chars))
        
        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)


class PasswordValidationCache:
    """
    Caching mechanism for password validation to improve performance.
    """
    
    CACHE_TIMEOUT = 300  # 5 minutes
    
    @staticmethod
    def get_validation_cache_key(password: str, user_id: Optional[int] = None) -> str:
        """Generate cache key for password validation."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()[:16]
        user_part = f"_{user_id}" if user_id else ""
        return f"pwd_validation_{password_hash}{user_part}"
    
    @classmethod
    def validate_password_cached(
        cls, 
        password: str, 
        user: Optional[User] = None
    ) -> Optional[List[ValidationError]]:
        """
        Validate password with caching for performance.
        
        Args:
            password: Password to validate
            user: User instance for context
            
        Returns:
            List of validation errors or None if valid
        """
        cache_key = cls.get_validation_cache_key(
            password, 
            user.id if user else None
        )
        
        # Check cache first
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Perform validation
        errors = []
        try:
            validate_password(password, user)
        except ValidationError as e:
            errors = e.error_list
        
        # Cache the result
        cache.set(cache_key, errors, cls.CACHE_TIMEOUT)
        
        return errors if errors else None


def check_password_breach(password: str) -> bool:
    """
    Check if password has been found in known data breaches.
    Uses k-anonymity with haveibeenpwned API.
    
    Args:
        password: Password to check
        
    Returns:
        True if password found in breach, False otherwise
    """
    import requests
    
    # Generate SHA-1 hash
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    try:
        # Query haveibeenpwned API
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            timeout=5
        )
        response.raise_for_status()
        
        # Check if our suffix appears in the response
        for line in response.text.splitlines():
            hash_suffix, count = line.split(':')
            if hash_suffix == suffix:
                return True
        
        return False
        
    except (requests.RequestException, ValueError):
        # If API is unavailable, don't block password creation
        return False


def get_password_policy_info() -> Dict[str, Any]:
    """
    Get current password policy information for display to users.
    
    Returns:
        Dictionary containing policy requirements
    """
    return {
        'min_length': 12,
        'requires_uppercase': True,
        'requires_lowercase': True,
        'requires_digits': True,
        'requires_special': True,
        'max_repeating': 3,
        'max_sequential': 3,
        'similarity_threshold': 0.7,
        'special_characters': "!@#$%^&*(),.?\":{}|<>",
        'help_text': [
            "Must be at least 12 characters long",
            "Must contain uppercase and lowercase letters",
            "Must contain at least one digit",
            "Must contain at least one special character",
            "Cannot be too similar to your personal information",
            "Cannot be a commonly used password",
            "Cannot contain more than 3 consecutive identical characters",
            "Cannot contain sequential characters (e.g., abc, 123)"
        ]
    }