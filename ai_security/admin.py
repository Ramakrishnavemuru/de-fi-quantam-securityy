from django.contrib import admin
from .models import SecurityAlert, AnomalyDetectionModel, SecurityScan

@admin.register(SecurityAlert)
class SecurityAlertAdmin(admin.ModelAdmin):
    list_display = ('alert_type', 'severity', 'user', 'timestamp', 'is_resolved')
    search_fields = ('description', 'user__email', 'transaction__tx_hash')
    list_filter = ('alert_type', 'severity', 'is_resolved', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(AnomalyDetectionModel)
class AnomalyDetectionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_type', 'version', 'created_at', 'is_active')
    search_fields = ('name', 'version')
    list_filter = ('model_type', 'is_active', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(SecurityScan)
class SecurityScanAdmin(admin.ModelAdmin):
    list_display = ('scan_type', 'status', 'started_at', 'completed_at', 'initiated_by')
    search_fields = ('results_summary', 'initiated_by__email')
    list_filter = ('scan_type', 'status', 'started_at')
    readonly_fields = ('started_at',)

