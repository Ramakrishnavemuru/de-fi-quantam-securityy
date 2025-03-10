from django.db import models
from accounts.models import User, Wallet

class Transaction(models.Model):
    """
    Represents a blockchain transaction with quantum-resistant signatures.
    """
    TRANSACTION_TYPES = (
        ('SEND', 'Send'),
        ('RECEIVE', 'Receive'),
        ('SWAP', 'Swap'),
        ('STAKE', 'Stake'),
        ('UNSTAKE', 'Unstake'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
    )
    
    tx_hash = models.CharField(max_length=255, unique=True)
    from_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sent_transactions')
    to_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=24, decimal_places=18)
    gas_fee = models.DecimalField(max_digits=24, decimal_places=18)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)
    block_number = models.IntegerField(null=True, blank=True)
    
    # Quantum-resistant signature fields
    signature = models.TextField()
    signature_algorithm = models.CharField(max_length=50, default="Dilithium")
    
    def __str__(self):
        return f"{self.tx_hash} - {self.amount} - {self.status}"

class SmartContract(models.Model):
    """
    Represents a deployed smart contract with quantum-resistant security.
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts')
    abi = models.JSONField()
    bytecode = models.TextField()
    creation_tx_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_quantum_resistant = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.address})"

class Token(models.Model):
    """
    Represents a token in the DeFi platform.
    """
    TOKEN_TYPES = (
        ('ERC20', 'ERC20'),
        ('ERC721', 'ERC721'),
        ('ERC1155', 'ERC1155'),
    )
    
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    contract = models.ForeignKey(SmartContract, on_delete=models.CASCADE, related_name='tokens')
    token_type = models.CharField(max_length=10, choices=TOKEN_TYPES)
    decimals = models.IntegerField(default=18)
    total_supply = models.DecimalField(max_digits=36, decimal_places=18)
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"

class TokenBalance(models.Model):
    """
    Represents a user's token balance.
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='token_balances')
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='balances')
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('wallet', 'token')
    
    def __str__(self):
        return f"{self.wallet.user.username} - {self.token.symbol}: {self.balance}"

