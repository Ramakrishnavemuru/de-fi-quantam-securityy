from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Transaction, SmartContract, Token, TokenBalance
from .serializers import TransactionSerializer, SmartContractSerializer, TokenSerializer, TokenBalanceSerializer
from .forms import TransactionForm, SmartContractForm
from .utils.ethereum import send_transaction, deploy_contract
from quantum_crypto.utils.key_management import sign_transaction_quantum
from ai_security.ml_models.anomaly_detection import check_transaction_anomaly

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for transactions
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        user_wallets = user.wallets.all()
        return Transaction.objects.filter(from_wallet__in=user_wallets)
    
    @action(detail=False, methods=['post'])
    def create_transaction(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check for anomalies using AI
            is_anomaly, confidence = check_transaction_anomaly(serializer.validated_data)
            if is_anomaly and confidence > 0.8:
                return Response({
                    'error': 'Potential security risk detected',
                    'details': 'This transaction has been flagged as anomalous',
                    'confidence': confidence
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Sign transaction with quantum-resistant algorithm
            wallet = get_object_or_404(request.user.wallets, id=serializer.validated_data['from_wallet'].id)
            signature = sign_transaction_quantum(serializer.validated_data, wallet)
            
            # Send transaction to blockchain
            tx_hash = send_transaction(serializer.validated_data, signature)
            
            # Save transaction with signature
            transaction = serializer.save(
                tx_hash=tx_hash,
                signature=signature['signature'],
                signature_algorithm=signature['algorithm']
            )
            
            return Response(self.get_serializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SmartContractViewSet(viewsets.ModelViewSet):
    """
    API endpoint for smart contracts
    """
    serializer_class = SmartContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SmartContract.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Deploy contract to blockchain
        contract_data = serializer.validated_data
        deployment_result = deploy_contract(contract_data)
        
        serializer.save(
            owner=self.request.user,
            address=deployment_result['address'],
            creation_tx_hash=deployment_result['tx_hash']
        )

class TokenViewSet(viewsets.ModelViewSet):
    """
    API endpoint for tokens
    """
    serializer_class = TokenSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Token.objects.all()

class TokenBalanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for token balances
    """
    serializer_class = TokenBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        user_wallets = user.wallets.all()
        return TokenBalance.objects.filter(wallet__in=user_wallets)

# Web views
@login_required
def transaction_list_view(request):
    user_wallets = request.user.wallets.all()
    transactions = Transaction.objects.filter(from_wallet__in=user_wallets).order_by('-timestamp')
    return render(request, 'blockchain/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_detail_view(request, tx_hash):
    user_wallets = request.user.wallets.all()
    transaction = get_object_or_404(Transaction, tx_hash=tx_hash, from_wallet__in=user_wallets)
    return render(request, 'blockchain/transaction_detail.html', {'transaction': transaction})

@login_required
def create_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction_data = form.cleaned_data
            
            # Check for anomalies using AI
            is_anomaly, confidence = check_transaction_anomaly(transaction_data)
            if is_anomaly and confidence > 0.8:
                messages.error(request, 'Transaction blocked: Potential security risk detected')
                return redirect('transaction_list')
            
            # Sign transaction with quantum-resistant algorithm
            wallet = transaction_data['from_wallet']
            signature = sign_transaction_quantum(transaction_data, wallet)
            
            # Send transaction to blockchain
            tx_hash = send_transaction(transaction_data, signature)
            
            # Save transaction
            transaction = form.save(commit=False)
            transaction.tx_hash = tx_hash
            transaction.signature = signature['signature']
            transaction.signature_algorithm = signature['algorithm']
            transaction.save()
            
            messages.success(request, 'Transaction submitted successfully')
            return redirect('transaction_detail', tx_hash=tx_hash)
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'blockchain/create_transaction.html', {'form': form})

@login_required
def smart_contract_list_view(request):
    contracts = SmartContract.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'blockchain/smart_contract_list.html', {'contracts': contracts})

@login_required
def deploy_smart_contract_view(request):
    if request.method == 'POST':
        form = SmartContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.owner = request.user
            
            # Deploy contract to blockchain
            deployment_result = deploy_contract({
                'name': contract.name,
                'abi': contract.abi,
                'bytecode': contract.bytecode
            })
            
            contract.address = deployment_result['address']
            contract.creation_tx_hash = deployment_result['tx_hash']
            contract.save()
            
            messages.success(request, 'Smart contract deployed successfully')
            return redirect('smart_contract_list')
    else:
        form = SmartContractForm()
    
    return render(request, 'blockchain/deploy_smart_contract.html', {'form': form})

