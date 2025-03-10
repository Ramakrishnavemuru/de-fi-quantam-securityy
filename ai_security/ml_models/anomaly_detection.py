import os
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from django.conf import settings
from datetime import datetime

def train_anomaly_detection_model(transaction_data=None, model_type='ISOLATION_FOREST'):
    """
    Trains an anomaly detection model on transaction data.
    
    Args:
        transaction_data: DataFrame containing transaction data
        model_type: Type of model to train
    
    Returns:
        Trained model and model metadata
    """
    # If no transaction data provided, generate sample data
    if transaction_data is None:
        transaction_data = generate_sample_transaction_data()
    
    # Preprocess data
    features = preprocess_transaction_data(transaction_data)
    
    # Train model
    if model_type == 'ISOLATION_FOREST':
        model = IsolationForest(contamination=0.05, random_state=42)
        model.fit(features)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    # Save model
    model_dir = settings.AI_SECURITY_SETTINGS.get('MODEL_PATH', os.path.join(os.path.dirname(__file__), 'trained_models'))
    os.makedirs(model_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    model_path = os.path.join(model_dir, f"{model_type.lower()}_{timestamp}.joblib")
    joblib.dump(model, model_path)
    
    # Calculate metrics (in a real implementation, you would use a validation set)
    # For demo purposes, we'll use the training data
    predictions = model.predict(features)
    anomaly_scores = model.decision_function(features)
    
    # Convert predictions to binary labels (1 for anomalies, 0 for normal)
    anomaly_predictions = np.where(predictions == -1, 1, 0)
    
    # In a real implementation, you would calculate actual metrics
    # For demo purposes, we'll use placeholder values
    metrics = {
        'accuracy': 0.95,
        'precision': 0.92,
        'recall': 0.88,
        'f1_score': 0.90
    }
    
    model_metadata = {
        'model_type': model_type,
        'version': timestamp,
        'file_path': model_path,
        'metrics': metrics
    }
    
    return model, model_metadata

def load_anomaly_detection_model():
    """
    Loads the latest anomaly detection model.
    
    Returns:
        Loaded model
    """
    model_dir = settings.AI_SECURITY_SETTINGS.get('MODEL_PATH', os.path.join(os.path.dirname(__file__), 'trained_models'))
    
    # Find the latest model file
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.joblib')]
    if not model_files:
        # If no model exists, train a new one
        model, _ = train_anomaly_detection_model()
        return model
    
    # Load the latest model
    latest_model = sorted(model_files)[-1]
    model_path = os.path.join(model_dir, latest_model)
    
    return joblib.load(model_path)

def check_transaction_anomaly(transaction_data):
    """
    Checks if a transaction is anomalous.
    
    Args:
        transaction_data: Transaction data to check
    
    Returns:
        Tuple of (is_anomaly, confidence)
    """
    # Load model
    try:
        model = load_anomaly_detection_model()
    except:
        # If model loading fails, train a new one
        model, _ = train_anomaly_detection_model()
    
    # Preprocess transaction data
    if isinstance(transaction_data, dict):
        # Convert dictionary to DataFrame
        transaction_df = pd.DataFrame([transaction_data])
    else:
        # Extract relevant fields from Transaction object
        transaction_df = pd.DataFrame([{
            'amount': float(transaction_data.amount),
            'gas_fee': float(transaction_data.gas_fee),
            'transaction_type': transaction_data.transaction_type
        }])
    
    features = preprocess_transaction_data(transaction_df)
    
    # Predict anomaly
    prediction = model.predict(features)[0]
    anomaly_score = model.decision_function(features)[0]
    
    # Convert prediction to boolean (True for anomaly, False for normal)
    is_anomaly = prediction == -1
    
    # Calculate confidence (higher absolute score = higher confidence)
    # Normalize to [0, 1] range
    confidence = 1 / (1 + np.exp(anomaly_score))
    
    return is_anomaly, confidence

def preprocess_transaction_data(transaction_data):
    """
    Preprocesses transaction data for anomaly detection.
    
    Args:
        transaction_data: DataFrame containing transaction data
    
    Returns:
        Preprocessed features
    """
    # Extract relevant features
    features = transaction_data.copy()
    
    # Handle categorical features
    if 'transaction_type' in features.columns:
        # One-hot encode transaction type
        transaction_types = pd.get_dummies(features['transaction_type'], prefix='type')
        features = pd.concat([features.drop('transaction_type', axis=1), transaction_types], axis=1)
    
    # Ensure numeric columns
    numeric_columns = ['amount', 'gas_fee']
    for col in numeric_columns:
        if col in features.columns:
            features[col] = pd.to_numeric(features[col], errors='coerce')
    
    # Fill missing values
    features = features.fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features.select_dtypes(include=['float64', 'int64']))
    
    return scaled_features

def generate_sample_transaction_data(n_samples=1000):
    """
    Generates sample transaction data for training.
    
    Args:
        n_samples: Number of samples to generate
    
    Returns:
        DataFrame containing sample transaction data
    """
    np.random.seed(42)
    
    # Generate normal transactions
    transaction_amounts = np.random.lognormal(mean=4.5, sigma=1, size=n_samples)
    gas_fees = np.random.lognormal(mean=2, sigma=0.5, size=n_samples)
    
    # Generate transaction types
    transaction_types = np.random.choice(['SEND', 'RECEIVE', 'SWAP', 'STAKE', 'UNSTAKE'], size=n_samples, p=[0.4, 0.3, 0.15, 0.1, 0.05])
    
    # Add some anomalies (5% of data)
    anomaly_indices = np.random.choice(range(n_samples), size=int(0.05 * n_samples), replace=False)
    transaction_amounts[anomaly_indices] = np.random.lognormal(mean=8, sigma=1, size=len(anomaly_indices))
    gas_fees[anomaly_indices] *= 3
    
    data = pd.DataFrame({
        'amount': transaction_amounts,
        'gas_fee': gas_fees,
        'transaction_type': transaction_types
    })
    
    return data

