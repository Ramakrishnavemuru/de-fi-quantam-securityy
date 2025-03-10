from rest_framework import serializers
from .models import SecurityAlert, AnomalyDetectionModel, SecurityScan

class SecurityAlertSerializer(serializers.ModelSerializer):
    transaction_hash = serializers.CharField(source='transaction.tx_hash', read_only=True)
    
    class Meta:
        model = SecurityAlert
        fields = ['id', 'user', 'transaction', 'transaction_hash', 'alert_type', 'severity', 
                  'description', 'timestamp', 'is_resolved', 'resolved_at', 
                  'resolved_by', 'resolution_notes']
        read_only_fields = ['timestamp', 'resolved_at']

class AnomalyDetectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyDetectionModel
        fields = ['id', 'name', 'model_type', 'version', 'created_at', 'is_active', 
                  'accuracy', 'precision', 'recall', 'f1_score']
        read_only_fields = ['created_at']

class SecurityScanSerializer(serializers.ModelSerializer):
    initiated_by_email = serializers.CharField(source='initiated_by.email', read_only=True)
    
    class Meta:
        model = SecurityScan
        fields = ['id', 'scan_type', 'status', 'started_at', 'completed_at', 
                  'initiated_by', 'initiated_by_email', 'results_summary', 
                  'issues_found', 'critical_issues']
        read_only_fields = ['started_at', 'completed_at', 'initiated_by']

