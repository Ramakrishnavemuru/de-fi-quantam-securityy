from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.security_dashboard_view, name='security_dashboard'),
    path('alerts/', views.alert_list_view, name='alert_list'),
    path('alerts/<int:alert_id>/', views.alert_detail_view, name='alert_detail'),
    path('scans/', views.scan_list_view, name='scan_list'),
    path('scans/start/', views.start_scan_view, name='start_scan'),
    path('analyze-transaction/', views.analyze_transaction_view, name='analyze_transaction'),
    path('analyze-transaction/<int:tx_id>/', views.analyze_transaction_view, name='analyze_transaction_by_id'),
]

