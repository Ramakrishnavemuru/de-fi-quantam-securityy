from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, Wallet, SecurityPreference
from .serializers import UserSerializer, WalletSerializer, SecurityPreferenceSerializer
from .forms import UserRegistrationForm, UserLoginForm, WalletCreationForm, SecurityPreferenceForm
from quantum_crypto.utils.key_management import generate_quantum_key_pair

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint for wallets
    """
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Generate quantum-resistant keys for the new wallet
        key_pair = generate_quantum_key_pair()
        serializer.save(
            user=self.request.user,
            public_key_hash=key_pair['public_key_hash'],
            key_algorithm=key_pair['algorithm']
        )

class SecurityPreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for security preferences
    """
    serializer_class = SecurityPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SecurityPreference.objects.filter(user=self.request.user)

# Web views
@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            
            # Create default security preferences
            SecurityPreference.objects.create(user=user)
            
            # Generate quantum keys for the user
            key_pair = generate_quantum_key_pair()
            user.quantum_key_id = key_pair['key_id']
            user.save()
            
            # Create default wallet
            Wallet.objects.create(
                user=user,
                address=f"0x{key_pair['public_key_hash']}",
                public_key_hash=key_pair['public_key_hash'],
                key_algorithm=key_pair['algorithm']
            )
            
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    wallets = Wallet.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', {'wallets': wallets})

@login_required
def create_wallet_view(request):
    if request.method == 'POST':
        form = WalletCreationForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            
            # Generate quantum-resistant keys for the new wallet
            key_pair = generate_quantum_key_pair()
            wallet.address = f"0x{key_pair['public_key_hash']}"
            wallet.public_key_hash = key_pair['public_key_hash']
            wallet.key_algorithm = key_pair['algorithm']
            wallet.save()
            
            messages.success(request, 'Wallet created successfully.')
            return redirect('dashboard')
    else:
        form = WalletCreationForm()
    
    return render(request, 'accounts/create_wallet.html', {'form': form})

@login_required
def security_preferences_view(request):
    security_prefs, created = SecurityPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SecurityPreferenceForm(request.POST, instance=security_prefs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Security preferences updated successfully.')
            return redirect('dashboard')
    else:
        form = SecurityPreferenceForm(instance=security_prefs)
    
    return render(request, 'accounts/security_preferences.html', {'form': form})

