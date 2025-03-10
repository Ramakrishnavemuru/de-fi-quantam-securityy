from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import SecurityAlert, AnomalyDetectionModel, SecurityScan
from .serializers import SecurityAlertSerializer, AnomalyDetectionModelSerializer, SecurityScanSerializer
from .ml_models.anomaly_detection import check_transaction_anomaly, train_anomaly_detection_model
from blockchain.models import Transaction

class SecurityAlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for security alerts
    """
    serializer_class = SecurityAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SecurityAlert.objects.filter(user=self.request.user).order_by('-timestamp')
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.resolution_notes = request.data.get('resolution_notes', '')
        alert.save()
        return Response(self.get_serializer(alert).data)

class SecurityScanViewSet(viewsets.ModelViewSet):
    """
    API endpoint for security scans
    """
    serializer_class = SecurityScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SecurityScan.objects.filter(initiated_by=self.request.user).order_by('-started_at')
    
    def perform_create(self, serializer):
        serializer.save(initiated_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def start_scan(self, request):
        scan_type = request.data.get('scan_type', 'FULL')
        
        # Create a new security scan
        scan = SecurityScan.objects.create(
            scan_type=scan_type,
            status='RUNNING',
            initiated_by=request.user
        )
        
        # In a real implementation, you would start the scan in a background task
        # For demo purposes, we'll simulate a completed scan
        scan.status = 'COMPLETED'
        scan.completed_at = timezone.now()
        scan.results_summary = f"Simulated {scan_type} scan completed successfully."
        scan.issues_found = 3
        scan.critical_issues = 1
        scan.save()
        
        return Response(self.get_serializer(scan).data, status=status.HTTP_201_CREATED)

# Web views
@login_required
def security_dashboard_view(request):
    alerts = SecurityAlert.objects.filter(user=request.user).order_by('-timestamp')[:10]
    scans = SecurityScan.objects.filter(initiated_by=request.user).order_by('-started_at')[:5]
    
    # Get statistics
    total_alerts = SecurityAlert.objects.filter(user=request.user).count()
    unresolved_alerts = SecurityAlert.objects.filter(user=request.user, is_resolved=False).count()
    critical_alerts = SecurityAlert.objects.filter(user=request.user, severity='CRITICAL', is_resolved=False).count()
    
    context = {
        'alerts': alerts,
        'scans': scans,
        'total_alerts': total_alerts,
        'unresolved_alerts': unresolved_alerts,
        'critical_alerts': critical_alerts,
    }
    
    return render(request, 'ai_security/dashboard.html', context)

@login_required
def alert_list_view(request):
    alerts = SecurityAlert.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'ai_security/alert_list.html', {'alerts': alerts})

@login_required
def alert_detail_view(request, alert_id):
    alert = get_object_or_404(SecurityAlert, id=alert_id, user=request.user)
    
    if request.method == 'POST':
        resolution_notes = request.POST.get('resolution_notes', '')
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.resolution_notes = resolution_notes
        alert.save()
        
        messages.success(request, 'Alert marked as resolved')
        return redirect('alert_list')
    
    return render(request, 'ai_security/alert_detail.html', {'alert': alert})

@login_required
def scan_list_view(request):
    scans = SecurityScan.objects.filter(initiated_by=request.user).order_by('-started_at')
    return render(request, 'ai_security/scan_list.html', {'scans': scans})

@login_required
def start_scan_view(request):
    if request.method == 'POST':
        scan_type = request.POST.get('scan_type', 'FULL')
        
        # Create a new security scan
        scan = SecurityScan.objects.create(
            scan_type=scan_type,
            status='RUNNING',
            initiated_by=request.user
        )
        
        # In a real implementation, you would start the scan in a background task
        # For demo purposes, we'll simulate a completed scan
        scan.status = 'COMPLETED'
        scan.completed_at = timezone.now()
        scan.results_summary = f"Simulated {scan_type} scan completed successfully."
        scan.issues_found = 3
        scan.critical_issues = 1
        scan.save()
        
        messages.success(request, 'Security scan completed')
        return redirect('scan_list')
    
    return render(request, 'ai_security/start_scan.html')

@login_required
def analyze_transaction_view(request, tx_id=None):
    if tx_id:
        transaction = get_object_or_404(Transaction, id=tx_id)
        
        # Check for anomalies
        is_anomaly, confidence = check_transaction_anomaly(transaction)
        
        if is_anomaly:
            # Create a security alert
            SecurityAlert.objects.create(
                user=request.user,
                transaction=transaction,
                alert_type='ANOMALY',
                severity='HIGH' if confidence > 0.8 else 'MEDIUM',
                description=f"Transaction {transaction.tx_hash} has been flagged as anomalous with {confidence:.2f} confidence."
            )
            
            messages.warning(request, f'Transaction flagged as anomalous with {confidence:.2f} confidence')
        else:
            messages.success(request, 'Transaction analysis completed. No anomalies detected.')
        
        return redirect('transaction_detail', tx_hash=transaction.tx_hash)
    
    # If no transaction ID provided, show a form to select a transaction
    user_wallets = request.user.wallets.all()
    transactions = Transaction.objects.filter(from_wallet__in=user_wallets).order_by('-timestamp')[:20]
    
    return render(request, 'ai_security/analyze_transaction.html', {'transactions': transactions})

