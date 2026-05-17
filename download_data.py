import os
import gzip
import shutil
import requests
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO

BASE_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/departements/{dept}.csv.gz"
INSEE_URL_TEMPLATE = ("https://bdm.insee.fr/series/010001868/csv?"
                      "lang=fr&ordre=antechronologique&transposition=donnees_colonne"
                      "&periodeDebut=1&anneeDebut={year_start}"
                      "&periodeFin=3&anneeFin={year_end}&revision=sans_revisions")

RAW_DIR = "./dataset_raw"
TMP_DIR = "./tmp_downloads"

DEPARTMENTS = ["77", "75"]  # Seine-et-Marne and Paris

# Wipe folders
shutil.rmtree(RAW_DIR, ignore_errors=True)
shutil.rmtree(TMP_DIR, ignore_errors=True)

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

current_year = datetime.now().year
downloaded_years = []

# Download data for each department
for dept in DEPARTMENTS:
    print(f"\n{'='*60}")
    print(f"Downloading data for department {dept}")
    print(f"{'='*60}")
    
    downloaded = 0
    year = 2024  # Start from 2024 instead of current year to avoid issues
    
    while downloaded < 5 and year >= 2020:
        url = BASE_URL.format(year=year, dept=dept)
        gz_path = os.path.join(TMP_DIR, f"{dept}_{year}.csv.gz")
        csv_path = os.path.join(RAW_DIR, f"{dept}_{year}.csv")

        print(f"\nTrying {year} → {url}")

        try:
            r = requests.get(url, stream=True, timeout=10)

            if r.status_code == 404:
                print(f"{year} not available for {dept}, skipping")
                year -= 1
                continue

            r.raise_for_status()

            print("Downloading...")
            with open(gz_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            print("Extracting CSV...")
            with gzip.open(gz_path, "rb") as f_in:
                with open(csv_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            downloaded_years.append(year)
            downloaded += 1
            year -= 1
        
        except Exception as e:
            print(f"Error downloading {year} for {dept}: {e}")
            year -= 1
            continue

print(f"\n{'='*60}")
print(f"Done. Downloaded datasets for years: {sorted(set(downloaded_years))}")
print(f"{'='*60}")

if downloaded_years:
    year_start = min(downloaded_years)
    year_end = max(downloaded_years)
    insee_url = INSEE_URL_TEMPLATE.format(year_start=year_start, year_end=year_end)

    print(f"\nDownloading INSEE indices ZIP for {year_start} to {year_end} → {insee_url}")
    r = requests.get(insee_url)
    r.raise_for_status()

    # Read ZIP from bytes
    with ZipFile(BytesIO(r.content)) as zip_file:
        # Extract only 'valeurs_trimestrielles.csv' to TMP_DIR
        if "valeurs_trimestrielles.csv" in zip_file.namelist():
            zip_file.extract("valeurs_trimestrielles.csv", TMP_DIR)
            print(f"Extracted 'valeurs_trimestrielles.csv' to {TMP_DIR}")
        else:
            print("Error: 'valeurs_trimestrielles.csv' not found in ZIP archive.")
else:
    print("No DVF datasets downloaded, skipping INSEE index download.")