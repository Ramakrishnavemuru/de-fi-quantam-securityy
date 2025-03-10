from rest_framework import serializers
from .models import Transaction, SmartContract, Token, TokenBalance

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'tx_hash', 'from_wallet', 'to_address', 'amount', 'gas_fee', 
                  'transaction_type', 'status', 'timestamp', 'block_number', 
                  'signature_algorithm']
        read_only_fields = ['tx_hash', 'status', 'timestamp', 'block_number', 'signature']

class SmartContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartContract
        fields = ['id', 'name', 'address', 'abi', 'bytecode', 'creation_tx_hash', 
                  'created_at', 'is_quantum_resistant']
        read_only_fields = ['address', 'creation_tx_hash', 'created_at']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['id', 'name', 'symbol', 'contract', 'token_type', 'decimals', 'total_supply']

class TokenBalanceSerializer(serializers.ModelSerializer):
    token_symbol = serializers.CharField(source='token.symbol', read_only=True)
    token_name = serializers.CharField(source='token.name', read_only=True)
    
    class Meta:
        model = TokenBalance
        fields = ['id', 'wallet', 'token', 'token_symbol', 'token_name', 'balance', 'last_updated']
        read_only_fields = ['last_updated']

