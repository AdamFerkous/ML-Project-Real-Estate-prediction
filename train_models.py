"""
Multi-department model training script
Trains separate Random Forest models for houses and apartments in 75 (Paris) and 77 (Seine-et-Marne)
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Configuration
DEPARTMENTS = ["77", "75"]
PROPERTY_TYPES = [("Maison", "maison"), ("Appartement", "appart")]

FEATURES = {
    "Maison": [
        "longitude",
        "latitude",
        "code_postal",
        "surface_reelle_bati",
        "nombre_pieces_principales",
        "prix_m2_ref",
        "surface_terrain",
        "number_of_lots",
        "season"
    ],
    "Appartement": [
        "longitude",
        "latitude",
        "code_postal",
        "surface_reelle_bati",
        "nombre_pieces_principales",
        "prix_m2_ref",
        "number_of_lots",
        "season"
    ]
}

TARGET = "valeur_fonciere_actualisee"

# Encoding for season
SEASON_MAPPING = {"winter": 0, "spring": 1, "summer": 2, "autumn": 3}

def train_model(property_type, dept):
    """Train a model for a specific property type and department"""
    print(f"\n{'='*70}")
    print(f"Training {property_type} model for department {dept}")
    print(f"{'='*70}")
    
    # Load data
    type_short = "appart" if property_type == "Appartement" else "maison"
    csv_file = f"datasets_prepd/dvf_{type_short}_{dept}.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return False
    
    df = pd.read_csv(csv_file)
    print(f"✓ Loaded {len(df)} records from {csv_file}")
    
    # Get features
    features = FEATURES[property_type]
    
    # Check for missing features
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        print(f"❌ Missing features: {missing_features}")
        return False
    
    # Prepare data
    df["season"] = df["season"].map(SEASON_MAPPING)
    
    X = df[features]
    y = df[TARGET]
    
    print(f"✓ Features: {X.shape[1]}, Samples: {X.shape[0]}")
    print(f"✓ Target range: €{y.min():,.0f} - €{y.max():,.0f}")
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y,
        test_size=0.3,
        random_state=42
    )
    
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp,
        test_size=0.5,
        random_state=42
    )
    
    print(f"✓ Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")
    
    # Save split data
    os.makedirs(f"data_{property_type.lower()}_{dept}", exist_ok=True)
    
    train_df = X_train.copy()
    val_df = X_val.copy()
    test_df = X_test.copy()
    
    train_df[TARGET] = y_train
    val_df[TARGET] = y_val
    test_df[TARGET] = y_test
    
    train_df.to_csv(f"data_{property_type.lower()}_{dept}/{property_type.lower()}_train.csv", index=False)
    val_df.to_csv(f"data_{property_type.lower()}_{dept}/{property_type.lower()}_val.csv", index=False)
    test_df.to_csv(f"data_{property_type.lower()}_{dept}/{property_type.lower()}_test.csv", index=False)
    
    print(f"✓ Train/Val/Test data saved")
    
    # Train model
    print(f"\nTraining Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print(f"✓ Model trained")
    
    # Validation evaluation
    y_val_pred = model.predict(X_val)
    val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
    val_mae = mean_absolute_error(y_val, y_val_pred)
    val_r2 = r2_score(y_val, y_val_pred)
    
    print(f"\nValidation metrics:")
    print(f"  RMSE: €{val_rmse:,.0f}")
    print(f"  MAE:  €{val_mae:,.0f}")
    print(f"  R²:   {val_r2:.4f}")
    
    # Test evaluation
    y_test_pred = model.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print(f"\nTest metrics:")
    print(f"  RMSE: €{test_rmse:,.0f}")
    print(f"  MAE:  €{test_mae:,.0f}")
    print(f"  R²:   {test_r2:.4f}")
    
    # Save model
    os.makedirs("models", exist_ok=True)
    model_path = f"models/{property_type.lower()}_rf_model_{dept}.pkl"
    joblib.dump(model, model_path)
    print(f"\n✓ Model saved to {model_path}")
    
    return True

def main():
    print("\n" + "="*70)
    print("MULTI-DEPARTMENT MODEL TRAINING")
    print("="*70)
    
    success_count = 0
    total_count = len(DEPARTMENTS) * len(PROPERTY_TYPES)
    
    for dept in DEPARTMENTS:
        for prop_type, prop_short in PROPERTY_TYPES:
            if train_model(prop_type, dept):
                success_count += 1
    
    print(f"\n{'='*70}")
    print(f"SUMMARY: {success_count}/{total_count} models trained successfully")
    print(f"{'='*70}\n")
    
    if success_count == total_count:
        print("✓ All models trained successfully!")
        return True
    else:
        print("❌ Some models failed")
        return False

if __name__ == "__main__":
    main()
