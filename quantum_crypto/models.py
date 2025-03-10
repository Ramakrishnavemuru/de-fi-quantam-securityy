from django.db import models
from accounts.models import User

class QuantumKey(models.Model):
    """
    Represents a quantum-resistant cryptographic key.
    """
    KEY_TYPES = (
        ('Kyber768', 'Kyber-768'),
        ('Kyber1024', 'Kyber-1024'),
        ('Dilithium2', 'Dilithium-2'),
        ('Dilithium3', 'Dilithium-3'),
        ('Falcon512', 'Falcon-512'),
        ('Falcon1024', 'Falcon-1024'),
    )
    
    key_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quantum_keys')
    key_type = models.CharField(max_length=20, choices=KEY_TYPES)
    public_key_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # The actual private key is never stored in the database
    # It's stored securely using the dKMS (Decentralized Key Management System)
    
    def __str__(self):
        return f"{self.key_type} - {self.key_id[:10]}..."

class KeyShare(models.Model):
    """
    Represents a share of a quantum key using threshold cryptography.
    """
    quantum_key = models.ForeignKey(QuantumKey, on_delete=models.CASCADE, related_name='shares')
    share_id = models.CharField(max_length=255)
    holder_identifier = models.CharField(max_length=255)  # Could be a server ID, node ID, etc.
    encrypted_share = models.TextField()  # Encrypted share data
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('quantum_key', 'share_id')
    
    def __str__(self):
        return f"Share {self.share_id} for {self.quantum_key.key_id[:10]}..."

class KeyUsageLog(models.Model):
    """
    Logs usage of quantum keys for auditing and security monitoring.
    """
    quantum_key = models.ForeignKey(QuantumKey, on_delete=models.CASCADE, related_name='usage_logs')
    operation = models.CharField(max_length=100)  # e.g., "sign_transaction", "encrypt_message"
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    success = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.operation} - {self.quantum_key.key_id[:10]}... - {self.timestamp}"

