import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from django.conf import settings

def train_threat_detection_model(data=None):
    """
    Trains a model to detect potential threats in blockchain transactions.
    
    Args:
        data: DataFrame containing labeled threat data
    
    Returns:
        Trained model and evaluation metrics
    """
    # If no data provided, generate sample data
    if data is None:
        data = generate_sample_threat_data()
    
    # Split data into features and target
    X = data.drop('is_threat', axis=1)
    y = data['is_threat']
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Save model
    model_dir = settings.AI_SECURITY_SETTINGS.get('MODEL_PATH', os.path.join(os.path.dirname(__file__), 'trained_models'))
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'threat_detection_model.joblib')
    joblib.dump(model, model_path)
    
    return model, {
        'accuracy': accuracy,
        'precision': report['1']['precision'],
        'recall': report['1']['recall'],
        'f1_score': report['1']['f1-score']
    }

def detect_threat(transaction_data):
    """
    Detects if a transaction poses a security threat.
    
    Args:
        transaction_data: Transaction data to analyze
    
    Returns:
        Tuple of (is_threat, confidence)
    """
    # Load model
    model_dir = settings.AI_SECURITY_SETTINGS.get('MODEL_PATH', os.path.join(os.path.dirname(__file__), 'trained_models'))
    model_path = os.path.join(model_dir, 'threat_detection_model.joblib')
    
    try:
        model = joblib.load(model_path)
    except:
        # If model doesn't exist, train a new one
        model, _ = train_threat_detection_model()
    
    # Preprocess transaction data
    features = preprocess_transaction_data(transaction_data)
    
    # Predict threat
    is_threat = model.predict(features)[0]
    
    # Get prediction probability
    confidence = model.predict_proba(features)[0][1]
    
    return bool(is_threat), confidence

def preprocess_transaction_data(transaction_data):
    """
    Preprocesses transaction data for threat detection.
    
    Args:
        transaction_data: Transaction data to preprocess
    
    Returns:
        Preprocessed features
    """
    # Convert to DataFrame if not already
    if not isinstance(transaction_data, pd.DataFrame):
        if isinstance(transaction_data, dict):
            transaction_data = pd.DataFrame([transaction_data])
        else:
            # Extract relevant fields from Transaction object
            transaction_data = pd.DataFrame([{
                'amount': float(transaction_data.amount),
                'gas_fee': float(transaction_data.gas_fee),
                'transaction_type': transaction_data.transaction_type,
                'to_address': transaction_data.to_address
            }])
    
    # Extract features
    features = transaction_data.copy()
    
    # Handle categorical features
    if 'transaction_type' in features.columns:
        # One-hot encode transaction type
        transaction_types = pd.get_dummies(features['transaction_type'], prefix='type')
        features = pd.concat([features.drop('transaction_type', axis=1), transaction_types], axis=1)
    
    # Add derived features
    if 'amount' in features.columns and 'gas_fee' in features.columns:
        features['fee_to_amount_ratio'] = features['gas_fee'] / features['amount'].replace(0, 1e-10)
    
    # Drop non-numeric columns that aren't needed for prediction
    if 'to_address' in features.columns:
        features.drop('to_address', axis=1, inplace=True)
    
    # Ensure all features are present that the model expects
    expected_features = ['amount', 'gas_fee', 'fee_to_amount_ratio', 
                         'type_SEND', 'type_RECEIVE', 'type_SWAP', 'type_STAKE', 'type_UNSTAKE']
    
    for feature in expected_features:
        if feature not in features.columns:
            if feature.startswith('type_'):
                features[feature] = 0
            else:
                features[feature] = 0
    
    return features

def generate_sample_threat_data(n_samples=1000):
    """
    Generates sample data for training the threat detection model.
    
    Args:
        n_samples: Number of samples to generate
    
    Returns:
        DataFrame containing sample data
    """
    np.random.seed(42)
    
    # Generate normal transactions
    transaction_amounts = np.random.lognormal(mean=4.5, sigma=1, size=n_samples)
    gas_fees = np.random.lognormal(mean=2, sigma=0.5, size=n_samples)
    transaction_types = np.random.choice(['SEND', 'RECEIVE', 'SWAP', 'STAKE', 'UNSTAKE'], size=n_samples)
    
    # Calculate fee to amount ratio
    fee_to_amount_ratio = gas_fees / transaction_amounts
    
    # Generate labels (10% threats)
    is_threat = np.zeros(n_samples, dtype=int)
    threat_indices = np.random.choice(range(n_samples), size=int(0.1 * n_samples), replace=False)
    is_threat[threat_indices] = 1
    
    # Modify threat transactions to have unusual characteristics
    transaction_amounts[threat_indices] = np.random.lognormal(mean=7, sigma=1.5, size=len(threat_indices))
    gas_fees[threat_indices] = np.random.lognormal(mean=4, sigma=1, size=len(threat_indices))
    fee_to_amount_ratio[threat_indices] = gas_fees[threat_indices] / transaction_amounts[threat_indices]
    
    # Create DataFrame
    data = pd.DataFrame({
        'amount': transaction_amounts,
        'gas_fee': gas_fees,
        'fee_to_amount_ratio': fee_to_amount_ratio,
        'transaction_type': transaction_types,
        'is_threat': is_threat
    })
    
    # One-hot encode transaction type
    transaction_types_encoded = pd.get_dummies(data['transaction_type'], prefix='type')
    data = pd.concat([data.drop('transaction_type', axis=1), transaction_types_encoded], axis=1)
    
    return data

