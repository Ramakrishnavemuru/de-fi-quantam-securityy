from django.contrib import admin
from .models import QuantumKey, KeyShare, KeyUsageLog

@admin.register(QuantumKey)
class QuantumKeyAdmin(admin.ModelAdmin):
    list_display = ('key_id', 'user', 'key_type', 'created_at', 'last_used', 'is_active')
    search_fields = ('key_id', 'user__email', 'public_key_hash')
    list_filter = ('key_type', 'is_active', 'created_at')
    readonly_fields = ('key_id', 'public_key_hash', 'created_at')

@admin.register(KeyShare)
class KeyShareAdmin(admin.ModelAdmin):
    list_display = ('quantum_key', 'share_id', 'holder_identifier', 'created_at')
    search_fields = ('quantum_key__key_id', 'share_id', 'holder_identifier')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(KeyUsageLog)
class KeyUsageLogAdmin(admin.ModelAdmin):
    list_display = ('quantum_key', 'operation', 'timestamp', 'ip_address', 'success')
    search_fields = ('quantum_key__key_id', 'operation', 'ip_address')
    list_filter = ('operation', 'success', 'timestamp')
    readonly_fields = ('timestamp',)

