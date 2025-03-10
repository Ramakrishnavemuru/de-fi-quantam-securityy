import json
from web3 import Web3
from django.conf import settings

def get_web3_instance():
    """
    Returns a Web3 instance connected to the Ethereum node.
    """
    provider_url = settings.BLOCKCHAIN_SETTINGS['ETHEREUM_NODE_URL']
    return Web3(Web3.HTTPProvider(provider_url))

def send_transaction(transaction_data, signature):
    """
    Sends a transaction to the Ethereum blockchain with quantum-resistant signature.
    
    Args:
        transaction_data: Dictionary containing transaction details
        signature: Dictionary containing quantum signature details
    
    Returns:
        tx_hash: Transaction hash
    """
    web3 = get_web3_instance()
    
    # Prepare transaction
    tx = {
        'from': transaction_data['from_wallet'].address,
        'to': transaction_data['to_address'],
        'value': web3.to_wei(float(transaction_data['amount']), 'ether'),
        'gas': 21000,  # Standard gas limit for ETH transfers
        'gasPrice': web3.to_wei(float(transaction_data['gas_fee']), 'gwei'),
        'nonce': web3.eth.get_transaction_count(transaction_data['from_wallet'].address),
        'chainId': settings.BLOCKCHAIN_SETTINGS['CHAIN_ID'],
        # Include quantum signature in the data field
        'data': web3.to_hex(text=f"QR-SIG:{signature['algorithm']}:{signature['signature'][:64]}...")
    }
    
    # In a real implementation, you would use the quantum signature
    # Here we're simulating with a standard Ethereum transaction
    # This is a placeholder for demonstration purposes
    
    # For demo purposes, we're returning a simulated tx_hash
    # In production, you would actually send the transaction and get a real tx_hash
    simulated_tx_hash = web3.keccak(text=f"{transaction_data['from_wallet'].address}:{transaction_data['to_address']}:{transaction_data['amount']}:{transaction_data['gas_fee']}:{signature['signature'][:10]}").hex()
    
    return simulated_tx_hash

def deploy_contract(contract_data):
    """
    Deploys a smart contract to the Ethereum blockchain.
    
    Args:
        contract_data: Dictionary containing contract details
    
    Returns:
        Dictionary with contract address and transaction hash
    """
    web3 = get_web3_instance()
    
    # In a real implementation, you would:
    # 1. Compile the contract or use the provided bytecode
    # 2. Create a contract instance
    # 3. Deploy it to the blockchain
    # 4. Return the contract address and transaction hash
    
    # For demo purposes, we're simulating deployment
    simulated_address = f"0x{web3.keccak(text=contract_data['name']).hex()[-40:]}"
    simulated_tx_hash = web3.keccak(text=f"deploy:{contract_data['name']}:{simulated_address}").hex()
    
    return {
        'address': simulated_address,
        'tx_hash': simulated_tx_hash
    }

def get_token_balance(wallet_address, token_contract_address):
    """
    Gets the token balance for a wallet.
    
    Args:
        wallet_address: Ethereum wallet address
        token_contract_address: Token contract address
    
    Returns:
        Token balance
    """
    web3 = get_web3_instance()
    
    # Standard ERC20 ABI for balanceOf function
    abi = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
    
    # Create contract instance
    contract = web3.eth.contract(address=token_contract_address, abi=abi)
    
    # Call balanceOf function
    balance = contract.functions.balanceOf(wallet_address).call()
    
    return balance

