from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Wallet, SecurityPreference

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

class WalletCreationForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name']

class SecurityPreferenceForm(forms.ModelForm):
    class Meta:
        model = SecurityPreference
        fields = ['two_factor_enabled', 'quantum_resistant_only', 'transaction_notifications', 'max_transaction_amount']
        widgets = {
            'max_transaction_amount': forms.NumberInput(attrs={'step': '0.000001'}),
        }

