from django.contrib import admin
from .models import Transaction, SmartContract, Token, TokenBalance

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('tx_hash', 'from_wallet', 'to_address', 'amount', 'transaction_type', 'status', 'timestamp')
    search_fields = ('tx_hash', 'from_wallet__address', 'to_address')
    list_filter = ('status', 'transaction_type', 'signature_algorithm')
    readonly_fields = ('tx_hash', 'signature', 'timestamp')

@admin.register(SmartContract)
class SmartContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner', 'created_at', 'is_quantum_resistant')
    search_fields = ('name', 'address', 'owner__email')
    list_filter = ('is_quantum_resistant', 'created_at')
    readonly_fields = ('address', 'creation_tx_hash', 'created_at')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'contract', 'token_type', 'total_supply')
    search_fields = ('name', 'symbol', 'contract__address')
    list_filter = ('token_type',)

@admin.register(TokenBalance)
class TokenBalanceAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'token', 'balance', 'last_updated')
    search_fields = ('wallet__address', 'token__name', 'token__symbol')
    list_filter = ('token__token_type', 'last_updated')

