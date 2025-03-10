from rest_framework import serializers
from .models import QuantumKey, KeyShare, KeyUsageLog

class QuantumKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantumKey
        fields = ['id', 'key_id', 'key_type', 'public_key_hash', 'created_at', 'last_used', 'is_active']
        read_only_fields = ['key_id', 'public_key_hash', 'created_at', 'last_used']

class KeyShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyShare
        fields = ['id', 'quantum_key', 'share_id', 'holder_identifier', 'created_at']
        read_only_fields = ['share_id', 'created_at']

class KeyUsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyUsageLog
        fields = ['id', 'quantum_key', 'operation', 'timestamp', 'ip_address', 'user_agent', 'success']
        read_only_fields = ['timestamp']

