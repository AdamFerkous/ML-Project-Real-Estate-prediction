"""
Test script for the Flask application
"""

import requests

# Test data for maison in Paris (75)
test_data_75_maison = {
    "form_type": "maison",
    "department": "75",
    "longitude": "2.35",
    "latitude": "48.85",
    "code_postal": "75001",
    "surface_reelle_bati": "100",
    "nombre_pieces_principales": "3",
    "prix_m2_ref": "10000",
    "surface_terrain": "100",
    "number_of_lots": "0",
    "season": "1"
}

# Test data for appartement in Seine-et-Marne (77)
test_data_77_appart = {
    "form_type": "appartement",
    "department": "77",
    "longitude": "2.5",
    "latitude": "48.5",
    "code_postal": "77001",
    "surface_reelle_bati": "70",
    "nombre_pieces_principales": "2",
    "prix_m2_ref": "2500",
    "number_of_lots": "1",
    "season": "2"
}

print("="*70)
print("TESTING FLASK APPLICATION")
print("="*70)

# Test 1: Maison in Paris (75)
print("\n[Test 1] Maison prediction in Paris (75)")
print("-" * 70)
try:
    response = requests.post("http://127.0.0.1:5000/", data=test_data_75_maison)
    if "Estimated Price" in response.text:
        print("✓ Prediction successful")
        # Extract price from HTML
        import re
        match = re.search(r'Estimated Price<br><br>\n(.+?)\s€', response.text)
        if match:
            price = match.group(1)
            print(f"  Predicted price: €{price}")
    else:
        print("❌ Prediction failed")
        if "error" in response.text.lower():
            print(f"  Error found in response")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Appartement in Seine-et-Marne (77)
print("\n[Test 2] Appartement prediction in Seine-et-Marne (77)")
print("-" * 70)
try:
    response = requests.post("http://127.0.0.1:5000/", data=test_data_77_appart)
    if "Estimated Price" in response.text:
        print("✓ Prediction successful")
        # Extract price from HTML
        import re
        match = re.search(r'Estimated Price<br><br>\n(.+?)\s€', response.text)
        if match:
            price = match.group(1)
            print(f"  Predicted price: €{price}")
    else:
        print("❌ Prediction failed")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("TESTING COMPLETE")
print("="*70)
