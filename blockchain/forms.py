from django import forms
from .models import Transaction, SmartContract

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['from_wallet', 'to_address', 'amount', 'gas_fee', 'transaction_type']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.000000000000000001'}),
            'gas_fee': forms.NumberInput(attrs={'step': '0.000000000000000001'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['from_wallet'].queryset = user.wallets.filter(is_active=True)

class SmartContractForm(forms.ModelForm):
    class Meta:
        model = SmartContract
        fields = ['name', 'abi', 'bytecode', 'is_quantum_resistant']
        widgets = {
            'abi': forms.Textarea(attrs={'rows': 10}),
            'bytecode': forms.Textarea(attrs={'rows': 5}),
        }

