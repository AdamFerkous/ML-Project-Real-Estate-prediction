"""
Comprehensive test script for all 4 models
"""

import requests
import re

# Test data combinations
test_cases = [
    {
        "name": "Maison in Paris (75)",
        "data": {
            "form_type": "maison",
            "department": "75",
            "longitude": "2.35",
            "latitude": "48.85",
            "code_postal": "75001",
            "surface_reelle_bati": "120",
            "nombre_pieces_principales": "4",
            "prix_m2_ref": "11000",
            "surface_terrain": "150",
            "number_of_lots": "0",
            "season": "1"
        }
    },
    {
        "name": "Appartement in Paris (75)",
        "data": {
            "form_type": "appartement",
            "department": "75",
            "longitude": "2.35",
            "latitude": "48.85",
            "code_postal": "75001",
            "surface_reelle_bati": "80",
            "nombre_pieces_principales": "3",
            "prix_m2_ref": "11000",
            "number_of_lots": "1",
            "season": "2"
        }
    },
    {
        "name": "Maison in Seine-et-Marne (77)",
        "data": {
            "form_type": "maison",
            "department": "77",
            "longitude": "2.5",
            "latitude": "48.5",
            "code_postal": "77001",
            "surface_reelle_bati": "100",
            "nombre_pieces_principales": "3",
            "prix_m2_ref": "2500",
            "surface_terrain": "800",
            "number_of_lots": "0",
            "season": "3"
        }
    },
    {
        "name": "Appartement in Seine-et-Marne (77)",
        "data": {
            "form_type": "appartement",
            "department": "77",
            "longitude": "2.5",
            "latitude": "48.5",
            "code_postal": "77001",
            "surface_reelle_bati": "70",
            "nombre_pieces_principales": "2",
            "prix_m2_ref": "2500",
            "number_of_lots": "1",
            "season": "0"
        }
    }
]

print("\n" + "="*80)
print("COMPREHENSIVE TEST - ALL 4 MODELS")
print("="*80)

success_count = 0
failed_tests = []

for i, test_case in enumerate(test_cases, 1):
    print(f"\n[Test {i}] {test_case['name']}")
    print("-" * 80)
    
    try:
        response = requests.post("http://127.0.0.1:5000/", data=test_case['data'], timeout=5)
        
        if "Estimated Price" in response.text:
            print(f"✓ Prediction successful")
            # Extract price from HTML
            match = re.search(r'Estimated Price<br><br>\n\s*([0-9,\.]+)\s*€', response.text)
            if match:
                price = match.group(1)
                print(f"  Predicted price: €{price}")
                success_count += 1
            else:
                print(f"⚠ Price not found in response")
                failed_tests.append(test_case['name'])
        elif "error" in response.text.lower() or "Error" in response.text:
            print(f"❌ Error in prediction")
            print(f"  Status code: {response.status_code}")
            failed_tests.append(test_case['name'])
        else:
            print(f"❌ Unexpected response")
            failed_tests.append(test_case['name'])
            
    except Exception as e:
        print(f"❌ Error: {e}")
        failed_tests.append(test_case['name'])

print("\n" + "="*80)
print(f"RESULTS: {success_count}/4 tests passed")
print("="*80)

if failed_tests:
    print(f"\nFailed tests:")
    for test in failed_tests:
        print(f"  - {test}")
else:
    print("\n✓ All tests passed successfully!")

print()
