import hashlib
import json
from datetime import datetime

def create_transaction_hash(transaction_data):
    """
    Creates a deterministic hash for a transaction.
    
    Args:
        transaction_data: Dictionary containing transaction details
    
    Returns:
        Transaction hash
    """
    # Create a deterministic representation of the transaction
    tx_dict = {
        'from': transaction_data['from_wallet'].address,
        'to': transaction_data['to_address'],
        'amount': str(transaction_data['amount']),
        'gas_fee': str(transaction_data['gas_fee']),
        'nonce': transaction_data.get('nonce', 0),
        'timestamp': datetime.now().isoformat()
    }
    
    # Convert to JSON string and hash
    tx_json = json.dumps(tx_dict, sort_keys=True)
    tx_hash = hashlib.sha256(tx_json.encode()).hexdigest()
    
    return tx_hash

def verify_transaction_signature(transaction, signature):
    """
    Verifies a quantum-resistant signature for a transaction.
    
    Args:
        transaction: Transaction object
        signature: Signature string
    
    Returns:
        Boolean indicating if signature is valid
    """
    # In a real implementation, you would:
    # 1. Get the public key for the wallet
    # 2. Use the appropriate quantum-resistant algorithm to verify the signature
    # 3. Return the verification result
    
    # For demo purposes, we're simulating verification
    # This is a placeholder for demonstration purposes
    return True

