"""
Model Training Module
Trains machine learning models for emergency prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from sklearn.neural_network import MLPClassifier
import pickle
import os
from datetime import datetime

def load_data(data_path='data/emergency_data.csv'):
    """Load and preprocess emergency data"""
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records from {data_path}")
    
    return df

def prepare_features(df):
    """
    Prepare features and target variable for training
    
    Features:
    - latitude, longitude
    - hour, day_of_week, month
    - temperature, humidity, wind_speed, precipitation, pressure
    - traffic_density, population_density
    
    Target:
    - emergency_occurred (binary: 0 or 1)
    """
    # Convert timestamp to datetime features
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
    
    # Define feature columns
    feature_columns = [
        'latitude', 'longitude',
        'hour', 'day_of_week', 'month',
        'temperature', 'humidity', 'wind_speed', 'precipitation', 'pressure',
        'traffic_density', 'population_density'
    ]
    
    # Ensure all feature columns exist
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns {missing_cols}")
        return None, None, None
    
    X = df[feature_columns].values
    y = df['emergency_occurred'].values
    
    return X, y, feature_columns

def train_emergency_model(data_path='data/emergency_data.csv', 
                         test_size=0.2, 
                         random_state=42,
                         model_type='Random Forest'):
    """
    Train emergency prediction model
    
    Args:
        data_path: Path to training data CSV
        test_size: Proportion of data for testing
        random_state: Random seed for reproducibility
        model_type: Type of model to train
    
    Returns:
        dict: Training results and metrics
    """
    print("=" * 60)
    print("EMERGENCY PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    df = load_data(data_path)
    if df is None:
        return None
    
    # Prepare features
    X, y, feature_names = prepare_features(df)
    if X is None:
        return None
    
    print(f"\nDataset shape: {X.shape}")
    print(f"Number of emergency cases: {y.sum()} ({y.sum()/len(y)*100:.1f}%)")
    print(f"Number of non-emergency cases: {len(y) - y.sum()} ({(len(y)-y.sum())/len(y)*100:.1f}%)")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Select and train model
    print(f"\nTraining {model_type} model...")
    
    if model_type == 'Random Forest':
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1
        )
    elif model_type == 'Gradient Boosting':
        model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=random_state
        )
    elif model_type == 'Neural Network':
        model = MLPClassifier(
            hidden_layer_sizes=(64, 32, 16),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=random_state,
            early_stopping=True
        )
    else:
        print(f"Unknown model type: {model_type}")
        return None
    
    # Train model
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    # Calculate metrics
    print("\n" + "=" * 60)
    print("TRAINING RESULTS")
    print("=" * 60)
    
    # Training metrics
    train_accuracy = accuracy_score(y_train, y_pred_train)
    print(f"\nTraining Set Performance:")
    print(f"Accuracy: {train_accuracy:.4f}")
    
    # Test metrics
    test_accuracy = accuracy_score(y_test, y_pred_test)
    test_precision = precision_score(y_test, y_pred_test, zero_division=0)
    test_recall = recall_score(y_test, y_pred_test, zero_division=0)
    test_f1 = f1_score(y_test, y_pred_test, zero_division=0)
    
    print(f"\nTest Set Performance:")
    print(f"Accuracy:  {test_accuracy:.4f}")
    print(f"Precision: {test_precision:.4f}")
    print(f"Recall:    {test_recall:.4f}")
    print(f"F1 Score:  {test_f1:.4f}")
    
    # ROC-AUC if model supports probability predictions
    if hasattr(model, 'predict_proba'):
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        test_roc_auc = roc_auc_score(y_test, y_pred_proba)
        print(f"ROC-AUC:   {test_roc_auc:.4f}")
    else:
        test_roc_auc = None
    
    # Detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_test, 
                                target_names=['No Emergency', 'Emergency']))
    
    # Feature importance (for tree-based models)
    feature_importance = None
    if hasattr(model, 'feature_importances_'):
        feature_importance = model.feature_importances_
        print("\nTop 5 Most Important Features:")
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)
        
        for idx, row in importance_df.head().iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")
    
    # Save model
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'emergency_model.pkl')
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names,
        'model_type': model_type,
        'trained_date': datetime.now().isoformat(),
        'metrics': {
            'accuracy': test_accuracy,
            'precision': test_precision,
            'recall': test_recall,
            'f1_score': test_f1,
            'roc_auc': test_roc_auc
        }
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✓ Model saved to {model_path}")
    print("=" * 60)
    
    # Return results
    results = {
        'accuracy': test_accuracy,
        'precision': test_precision,
        'recall': test_recall,
        'f1_score': test_f1,
        'roc_auc': test_roc_auc,
        'feature_names': feature_names,
        'feature_importance': feature_importance.tolist() if feature_importance is not None else None
    }
    
    return results

def evaluate_model(model_path='models/emergency_model.pkl', 
                  data_path='data/emergency_data.csv'):
    """
    Evaluate a trained model on test data
    
    Args:
        model_path: Path to saved model
        data_path: Path to evaluation data
    
    Returns:
        dict: Evaluation metrics
    """
    # Load model
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return None
    
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
        model = model_data['model']
        scaler = model_data['scaler']
    
    # Load data
    df = load_data(data_path)
    if df is None:
        return None
    
    X, y, _ = prepare_features(df)
    if X is None:
        return None
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Make predictions
    y_pred = model.predict(X_scaled)
    
    # Calculate metrics
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, zero_division=0)
    recall = recall_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)
    
    print("\nModel Evaluation Results:")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

if __name__ == "__main__":
    # Train model with default parameters
    results = train_emergency_model()
    
    if results:
        print("\nTraining completed successfully!")
    else:
        print("\nTraining failed. Please check the data and try again.")