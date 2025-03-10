from rest_framework import serializers
from .models import User, Wallet, SecurityPreference

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_verified', 'date_joined']
        read_only_fields = ['date_joined', 'is_verified']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'address', 'name', 'balance', 'is_active', 'created_at', 'updated_at', 'key_algorithm']
        read_only_fields = ['address', 'balance', 'created_at', 'updated_at', 'public_key_hash']

class SecurityPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPreference
        fields = ['id', 'two_factor_enabled', 'quantum_resistant_only', 'transaction_notifications', 'max_transaction_amount']

