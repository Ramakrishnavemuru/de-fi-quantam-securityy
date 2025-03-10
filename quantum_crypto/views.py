from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import QuantumKey, KeyShare, KeyUsageLog
from .serializers import QuantumKeySerializer, KeyShareSerializer, KeyUsageLogSerializer
from .utils.key_management import generate_quantum_key_pair, rotate_quantum_key

class QuantumKeyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for quantum keys
    """
    serializer_class = QuantumKeySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return QuantumKey.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_key(self, request):
        key_type = request.data.get('key_type', 'Kyber768')
        
        # Generate new quantum key pair
        key_data = generate_quantum_key_pair(key_type=key_type)
        
        # Create QuantumKey object
        quantum_key = QuantumKey.objects.create(
            key_id=key_data['key_id'],
            user=request.user,
            key_type=key_type,
            public_key_hash=key_data['public_key_hash']
        )
        
        # Create key shares (in a real implementation, these would be distributed)
        for i, share in enumerate(key_data['shares']):
            KeyShare.objects.create(
                quantum_key=quantum_key,
                share_id=f"share_{i+1}",
                holder_identifier=f"node_{i+1}",
                encrypted_share=share
            )
        
        return Response(self.get_serializer(quantum_key).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def rotate_key(self, request, pk=None):
        quantum_key = self.get_object()
        
        # Rotate the quantum key
        new_key_data = rotate_quantum_key(quantum_key)
        
        # Update the QuantumKey object
        quantum_key.key_id = new_key_data['key_id']
        quantum_key.public_key_hash = new_key_data['public_key_hash']
        quantum_key.save()
        
        # Delete old shares and create new ones
        quantum_key.shares.all().delete()
        for i, share in enumerate(new_key_data['shares']):
            KeyShare.objects.create(
                quantum_key=quantum_key,
                share_id=f"share_{i+1}",
                holder_identifier=f"node_{i+1}",
                encrypted_share=share
            )
        
        return Response(self.get_serializer(quantum_key).data)

# Web views
@login_required
def quantum_key_list_view(request):
    keys = QuantumKey.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'quantum_crypto/key_list.html', {'keys': keys})

@login_required
def generate_quantum_key_view(request):
    if request.method == 'POST':
        key_type = request.POST.get('key_type', 'Kyber768')
        
        # Generate new quantum key pair
        key_data = generate_quantum_key_pair(key_type=key_type)
        
        # Create QuantumKey object
        quantum_key = QuantumKey.objects.create(
            key_id=key_data['key_id'],
            user=request.user,
            key_type=key_type,
            public_key_hash=key_data['public_key_hash']
        )
        
        # Create key shares (in a real implementation, these would be distributed)
        for i, share in enumerate(key_data['shares']):
            KeyShare.objects.create(
                quantum_key=quantum_key,
                share_id=f"share_{i+1}",
                holder_identifier=f"node_{i+1}",
                encrypted_share=share
            )
        
        messages.success(request, f'New {key_type} quantum key generated successfully')
        return redirect('quantum_key_list')
    
    return render(request, 'quantum_crypto/generate_key.html')

@login_required
def rotate_quantum_key_view(request, key_id):
    quantum_key = get_object_or_404(QuantumKey, key_id=key_id, user=request.user)
    
    if request.method == 'POST':
        # Rotate the quantum key
        new_key_data = rotate_quantum_key(quantum_key)
        
        # Update the QuantumKey object
        quantum_key.key_id = new_key_data['key_id']
        quantum_key.public_key_hash = new_key_data['public_key_hash']
        quantum_key.save()
        
        # Delete old shares and create new ones
        quantum_key.shares.all().delete()
        for i, share in enumerate(new_key_data['shares']):
            KeyShare.objects.create(
                quantum_key=quantum_key,
                share_id=f"share_{i+1}",
                holder_identifier=f"node_{i+1}",
                encrypted_share=share
            )
        
        messages.success(request, 'Quantum key rotated successfully')
        return redirect('quantum_key_list')
    
    return render(request, 'quantum_crypto/rotate_key.html', {'key': quantum_key})

