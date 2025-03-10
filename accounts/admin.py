from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Wallet, SecurityPreference

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_verified', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Quantum Security', {'fields': ('quantum_key_id', 'is_verified')}),
    )

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('address', 'name', 'user', 'balance', 'is_active', 'created_at')
    search_fields = ('address', 'name', 'user__email')
    list_filter = ('is_active', 'key_algorithm')

@admin.register(SecurityPreference)
class SecurityPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'two_factor_enabled', 'quantum_resistant_only', 'transaction_notifications')
    search_fields = ('user__email',)
    list_filter = ('two_factor_enabled', 'quantum_resistant_only', 'transaction_notifications')

