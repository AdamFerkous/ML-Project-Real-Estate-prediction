"""
Generate synthetic test data for the real estate prediction project
This creates sample datasets for Paris (75) and Seine-et-Marne (77)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

np.random.seed(42)

RAW_DIR = "./dataset_raw"
os.makedirs(RAW_DIR, exist_ok=True)

# Generate test data for both departments
DEPARTMENTS = {
    "77": {
        "code_postal_prefix": 77,
        "price_range": (150000, 600000),  # Seine-et-Marne prices
        "price_m2_range": (1500, 3500),
        "surface_range": (60, 250),
        "terrain_range": (500, 5000)
    },
    "75": {
        "code_postal_prefix": 75,
        "price_range": (250000, 1500000),  # Paris prices (higher)
        "price_m2_range": (5000, 15000),
        "surface_range": (30, 150),
        "terrain_range": (10, 500)  # Much smaller in Paris
    }
}

# Common columns for DVF data
COLUMNS = [
    "date_mutation",
    "nature_mutation",
    "type_local",
    "code_postal",
    "longitude",
    "latitude",
    "valeur_fonciere",
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "surface_terrain",
    "lot1_numero", "lot2_numero", "lot3_numero", "lot4_numero", "lot5_numero",
    "lot1_surface_carrez", "lot2_surface_carrez", "lot3_surface_carrez", "lot4_surface_carrez", "lot5_surface_carrez"
]

# Generate data for each year
for dept, config in DEPARTMENTS.items():
    print(f"\nGenerating test data for department {dept}...")
    
    for year in range(2020, 2025):
        data = []
        n_records = 2000  # 2000 records per department per year
        
        for _ in range(n_records):
            # Generate date
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            random_date = start_date + timedelta(days=np.random.randint(0, 365))
            
            # Random property type
            prop_type = np.random.choice(["Maison", "Appartement"], p=[0.6, 0.4])
            
            # Price calculation
            price_m2 = np.random.uniform(config["price_m2_range"][0], config["price_m2_range"][1])
            surface = np.random.uniform(config["surface_range"][0], config["surface_range"][1])
            price = price_m2 * surface + np.random.normal(0, price_m2 * surface * 0.15)
            
            # Ensure price is positive
            price = max(1000, price)
            
            # Surface terrain (only for houses)
            if prop_type == "Maison":
                surface_terrain = np.random.uniform(config["terrain_range"][0], config["terrain_range"][1])
            else:
                surface_terrain = np.nan
            
            # Postal code
            postal_variants = [f"{config['code_postal_prefix']}0{i}" for i in range(20)]
            postal_code = np.random.choice(postal_variants)
            
            # Coordinates (approximate for department)
            if dept == "77":
                lon = np.random.uniform(2.0, 3.5)
                lat = np.random.uniform(48.0, 49.0)
            else:  # 75
                lon = np.random.uniform(2.22, 2.48)
                lat = np.random.uniform(48.81, 48.90)
            
            # Number of rooms
            pieces = np.random.randint(1, 7)
            
            # Lot information (for apartments)
            lot_data = {}
            for i in range(1, 6):
                if np.random.random() < 0.3:
                    lot_data[f"lot{i}_numero"] = np.random.randint(1, 1000)
                    if prop_type == "Appartement":
                        lot_data[f"lot{i}_surface_carrez"] = np.random.uniform(10, 100)
                    else:
                        lot_data[f"lot{i}_surface_carrez"] = np.nan
                else:
                    lot_data[f"lot{i}_numero"] = np.nan
                    lot_data[f"lot{i}_surface_carrez"] = np.nan
            
            record = {
                "date_mutation": random_date.strftime("%Y-%m-%d"),
                "nature_mutation": "Vente",
                "type_local": prop_type,
                "code_postal": postal_code,
                "longitude": lon,
                "latitude": lat,
                "valeur_fonciere": price,
                "surface_reelle_bati": surface,
                "nombre_pieces_principales": pieces,
                "surface_terrain": surface_terrain,
                **lot_data
            }
            
            data.append(record)
        
        # Save to CSV
        df = pd.DataFrame(data)
        filename = os.path.join(RAW_DIR, f"{dept}_{year}.csv")
        df.to_csv(filename, index=False)
        print(f"✓ Generated {filename} ({len(df)} records)")

print("\n✓ Test data generation complete!")
print(f"✓ Data saved to {RAW_DIR}")
