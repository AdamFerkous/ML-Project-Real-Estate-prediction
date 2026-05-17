"""
Generate synthetic INSEE indices for testing
"""

import pandas as pd
import os
from datetime import datetime

TMP_DIR = "./tmp_downloads"
os.makedirs(TMP_DIR, exist_ok=True)

# Create synthetic INSEE indices data
# Base 100 in 2015-T1
data = []

for year in range(2020, 2025):
    for quarter in range(1, 5):
        # Simulate price increases over time
        base_increase = (year - 2015) * 2  # ~2% per year
        quarterly_variation = (quarter - 1) * 0.5  # Small variation by quarter
        indice = 100 + base_increase + quarterly_variation + (year - 2020) * 0.8
        
        data.append({
            "Codes": "FR",
            "Libellé": f"{year}-T{quarter}",
            "Indice des prix des logements (neufs et anciens) – Brut – Base 100 en moyenne annuelle 2015": round(indice, 2)
        })

df = pd.DataFrame(data)
output_path = os.path.join(TMP_DIR, "valeurs_trimestrielles.csv")
df.to_csv(output_path, index=False, sep=";")

print(f"✓ Generated INSEE data: {output_path}")
print(df.head(10))
