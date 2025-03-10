from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('transactions/<str:tx_hash>/', views.transaction_detail_view, name='transaction_detail'),
    path('transactions/create/', views.create_transaction_view, name='create_transaction'),
    path('smart-contracts/', views.smart_contract_list_view, name='smart_contract_list'),
    path('smart-contracts/deploy/', views.deploy_smart_contract_view, name='deploy_smart_contract'),
]

