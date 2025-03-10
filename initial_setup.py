"""
This script sets up initial data for the Quantum-Resistant DeFi platform.
Run this after migrations to create test wallets and initial AI models.
"""
import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantum_defi.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Wallet, SecurityPreference
from blockchain.models import Transaction, Token
from quantum_crypto.models import QuantumKey
from quantum_crypto.utils.key_management import generate_quantum_key_pair
from ai_security.ml_models.anomaly_detection import train_anomaly_detection_model

User = get_user_model()

def setup_test_users():
    """Create test users with wallets"""
    print("Creating test users and wallets...")
    
    # Create test users if they don't exist
    user1, created1 = User.objects.get_or_create(
        username="alice",
        email="alice@example.com",
        defaults={
            'is_active': True,
            'is_verified': True
        }
    )
    
    if created1:
        user1.set_password("password123")
        user1.save()
        print(f"Created user: {user1.username}")
    
    user2, created2 = User.objects.get_or_create(
        username="bob",
        email="bob@example.com",
        defaults={
            'is_active': True,
            'is_verified': True
        }
    )
    
    if created2:
        user2.set_password("password123")
        user2.save()
        print(f"Created user: {user2.username}")
    
    # Create security preferences
    for user in [user1, user2]:
        SecurityPreference.objects.get_or_create(
            user=user,
            defaults={
                'two_factor_enabled': False,
                'quantum_resistant_only': True,
                'transaction_notifications': True
            }
        )
    
    # Create quantum keys and wallets
    for user in [user1, user2]:
        # Check if user already has wallets
        if not Wallet.objects.filter(user=user).exists():
            # Generate quantum key
            key_data = generate_quantum_key_pair()
            
            # Create quantum key record
            quantum_key, created = QuantumKey.objects.get_or_create(
                key_id=key_data['key_id'],
                user=user,
                defaults={
                    'key_type': key_data['algorithm'],
                    'public_key_hash': key_data['public_key_hash'],
                    'is_active': True
                }
            )
            
            # Create wallet
            wallet = Wallet.objects.create(
                user=user,
                address=f"0x{key_data['public_key_hash']}",
                name=f"{user.username}'s Main Wallet",
                balance=Decimal(str(random.uniform(1.0, 10.0))),
                public_key_hash=key_data['public_key_hash'],
                key_algorithm=key_data['algorithm']
            )
            
            print(f"Created wallet for {user.username}: {wallet.address}")

def setup_ai_models():
    """Train and set up initial AI models"""
    print("Setting up AI security models...")
    
    # Train anomaly detection model
    model, metadata = train_anomaly_detection_model()
    
    print(f"Trained anomaly detection model: {metadata['model_type']} v{metadata['version']}")
    print(f"Model accuracy: {metadata['metrics']['accuracy']:.2f}")

def create_sample_transactions():
    """Create some sample transactions between wallets"""
    print("Creating sample transactions...")
    
    # Get users
    try:
        alice = User.objects.get(username="alice")
        bob = User.objects.get(username="bob")
        
        alice_wallet = Wallet.objects.filter(user=alice).first()
        bob_wallet = Wallet.objects.filter(user=bob).first()
        
        if alice_wallet and bob_wallet:
            # Create a transaction from Alice to Bob
            tx1 = Transaction.objects.create(
                tx_hash=f"0x{os.urandom(32).hex()}",
                from_wallet=alice_wallet,
                to_address=bob_wallet.address,
                amount=Decimal('0.5'),
                gas_fee=Decimal('0.001'),
                transaction_type='SEND',
                status='CONFIRMED',
                signature=f"sig_{os.urandom(16).hex()}",
                signature_algorithm="Dilithium"
            )
            
            # Create a transaction from Bob to Alice
            tx2 = Transaction.objects.create(
                tx_hash=f"0x{os.urandom(32).hex()}",
                from_wallet=bob_wallet,
                to_address=alice_wallet.address,
                amount=Decimal('0.25'),
                gas_fee=Decimal('0.001'),
                transaction_type='SEND',
                status='CONFIRMED',
                signature=f"sig_{os.urandom(16).hex()}",
                signature_algorithm="Dilithium"
            )
            
            print(f"Created transaction from {alice.username} to {bob.username}: {tx1.tx_hash}")
            print(f"Created transaction from {bob.username} to {alice.username}: {tx2.tx_hash}")
    except User.DoesNotExist:
        print("Users not found. Run setup_test_users first.")

if __name__ == "__main__":
    setup_test_users()
    setup_ai_models()
    create_sample_transactions()
    print("Initial setup complete!")

