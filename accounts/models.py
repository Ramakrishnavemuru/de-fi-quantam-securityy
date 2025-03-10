from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model for the quantum-resistant DeFi platform.
    Extends Django's AbstractUser to add additional fields.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    quantum_key_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Required for Django's AbstractUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class Wallet(models.Model):
    """
    Represents a user's cryptocurrency wallet with quantum-resistant keys.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    address = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100, default="Main Wallet")
    balance = models.DecimalField(max_digits=24, decimal_places=18, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Quantum-resistant key references
    public_key_hash = models.CharField(max_length=255)
    key_algorithm = models.CharField(max_length=50, default="Kyber768")
    
    def __str__(self):
        return f"{self.name} ({self.address})"

class SecurityPreference(models.Model):
    """
    User security preferences for the platform.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_preferences')
    two_factor_enabled = models.BooleanField(default=False)
    quantum_resistant_only = models.BooleanField(default=True)
    transaction_notifications = models.BooleanField(default=True)
    max_transaction_amount = models.DecimalField(max_digits=24, decimal_places=18, null=True, blank=True)
    
    def __str__(self):
        return f"Security Preferences for {self.user.email}"

