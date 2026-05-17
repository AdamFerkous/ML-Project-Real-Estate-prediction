# Real Estate Price Prediction

This project builds machine learning models to predict real estate
prices for **houses (maisons)** and **apartments (appartements)** in two French regions:
- **Paris (75)** 
- **Seine-et-Marne (77)**

Using historical French real estate transaction data.

The repository contains a complete machine learning pipeline including:

-   Data acquisition for multiple departments
-   Data preparation and feature engineering
-   Model training for different property types in each department
-   A Flask web application for testing predictions with department selection

------------------------------------------------------------------------

# Project Overview

The workflow of the project is organized as follows:

1.  Download historical property transaction data from two departments
2.  Clean and prepare datasets separated by department
3.  Train separate machine learning models for:
    - Houses (Maisons) in Paris (75)
    - Apartments (Appartements) in Paris (75)
    - Houses (Maisons) in Seine-et-Marne (77)
    - Apartments (Appartements) in Seine-et-Marne (77)
4.  Deploy a local Flask application to generate predictions by department

------------------------------------------------------------------------

# Installation

Clone the repository and install the required dependencies.

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# Data Acquisition

Download the raw datasets by running:

``` bash
python download_data.py
```

This script will:

-   Download real estate transaction datasets for **both departments (75 and 77)**
-   Download the **last five years** of data
-   Store downloaded archives in:
    - tmp_downloads/
-   Extract CSV files into:
    - dataset_raw/

The datasets are automatically separated by department code in the filenames:
- `75_YYYY.csv` - Paris data
- `77_YYYY.csv` - Seine-et-Marne data

------------------------------------------------------------------------

# Data Preparation

Run the data preparation notebook:

    prep_data.ipynb

This notebook performs:

-   Data cleaning and filtering
-   Feature engineering (price per m², season, etc.)
-   Property type separation
-   **Department-based separation** (75 vs 77)
-   Dataset preparation for training

Prepared datasets are saved in `datasets_prepd/` with the following structure:

-   `dvf_maison_75.csv` - Houses in Paris
-   `dvf_appart_75.csv` - Apartments in Paris
-   `dvf_maison_77.csv` - Houses in Seine-et-Marne
-   `dvf_appart_77.csv` - Apartments in Seine-et-Marne

------------------------------------------------------------------------

# Model Training

Run the training script to train all 4 models:

``` bash
python train_models.py
```

This will train and save:

### Paris (75) Models

-   `models/maison_rf_model_75.pkl` - House prediction model
-   `models/appartement_rf_model_75.pkl` - Apartment prediction model

### Seine-et-Marne (77) Models

-   `models/maison_rf_model_77.pkl` - House prediction model
-   `models/appartement_rf_model_77.pkl` - Apartment prediction model

### Training Outputs

Processed datasets for each model are saved in:

    data_maison_75/
    data_appart_75/
    data_maison_77/
    data_appart_77/

Each containing:
- `*_train.csv` - Training data
- `*_val.csv` - Validation data
- `*_test.csv` - Test data

------------------------------------------------------------------------

# Web Application

Run the Flask web application:

``` bash
python app.py
```

Then open your browser to: **http://127.0.0.1:5000**

### Features

- **Department Selection**: Choose between Paris (75) or Seine-et-Marne (77)
- **Property Type**: Select between House (Maison) or Apartment (Appartement)
- **Address Geocoding**: Enter a French address to automatically get GPS coordinates
- **Price Prediction**: Get AI-powered price estimates

### Example Usage

1. Select a department (Paris or Seine-et-Marne)
2. Click "Maison" or "Appartement"
3. (Optional) Enter an address to get coordinates automatically
4. Fill in the property details
5. Click "Predict Price"

------------------------------------------------------------------------

# Project Structure

```
.
├── app.py                           # Flask web application
├── download_data.py                 # Download DVF data for multiple departments
├── prep_data.ipynb                  # Data preparation notebook
├── train_models.py                  # Script to train all 4 models
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── dataset_raw/                     # Raw downloaded data (separate by dept)
│   ├── 75_2020.csv ... 75_2024.csv  # Paris data
│   └── 77_2020.csv ... 77_2024.csv  # Seine-et-Marne data
│
├── datasets_prepd/                  # Prepared datasets (split by dept)
│   ├── dvf_maison_75.csv
│   ├── dvf_appart_75.csv
│   ├── dvf_maison_77.csv
│   └── dvf_appart_77.csv
│
├── data_maison_75/                  # Training data for Paris houses
├── data_appart_75/                  # Training data for Paris apartments
├── data_maison_77/                  # Training data for Seine-et-Marne houses
├── data_appart_77/                  # Training data for Seine-et-Marne apartments
│
├── models/                          # Trained models
│   ├── maison_rf_model_75.pkl
│   ├── appartement_rf_model_75.pkl
│   ├── maison_rf_model_77.pkl
│   └── appartement_rf_model_77.pkl
│
└── templates/
    └── index.html                   # Web interface
```

------------------------------------------------------------------------

# Key Differences: Paris vs Seine-et-Marne

The models account for significant differences between these regions:

| Aspect | Paris (75) | Seine-et-Marne (77) |
|--------|-----------|-------------------|
| Avg House Price | €1.0M - €1.7M | €150K - €600K |
| Avg Apartment Price | €210K - €1.7M | €150K - €968K |
| Avg Price/m² | €5,000 - €15,000 | €1,500 - €3,500 |
| Land Size | Very small | Larger plots |
| Model Type | Separate RF model | Separate RF model |

------------------------------------------------------------------------

# Testing

Run the comprehensive test suite:

``` bash
# Test all 4 models
python test_all_models.py
```

This tests:
- Maison prediction in Paris (75)
- Appartement prediction in Paris (75)
- Maison prediction in Seine-et-Marne (77)
- Appartement prediction in Seine-et-Marne (77)

------------------------------------------------------------------------

# Technical Stack

-   **Data Processing**: Pandas, NumPy
-   **Machine Learning**: Scikit-learn (Random Forest Regressor)
-   **Web Framework**: Flask
-   **Geocoding**: OpenStreetMap Nominatim API

------------------------------------------------------------------------

# Model Performance

Typical performance metrics on test data:

**Paris (75) - Houses**
- RMSE: €232,566
- MAE: €190,238
- R²: 0.5707

**Paris (75) - Apartments**
- RMSE: €229,945
- MAE: €190,871
- R²: 0.5862

**Seine-et-Marne (77) - Houses**
- RMSE: €105,973
- MAE: €84,280
- R²: 0.5934

**Seine-et-Marne (77) - Apartments**
- RMSE: €106,012
- MAE: €84,613
- R²: 0.5727

------------------------------------------------------------------------

# Data Sources

-   **DVF Data**: French Government Real Estate Transaction Data
    - https://files.data.gouv.fr/geo-dvf/
-   **INSEE Price Indices**: French National Statistics Office
    - https://www.insee.fr/

------------------------------------------------------------------------

# Notes

- All models use the same feature set (with adjustments for property type)
- Prix/m² reference is calculated per postal code
- Data is adjusted for inflation using INSEE indices
- Season feature (winter/spring/summer/autumn) helps capture temporal patterns

------------------------------------------------------------------------

# Running the Web Application

After completing the previous steps, launch the Flask application:

``` bash
python app.py
```

The application will start locally at:

    http://127.0.0.1:5000

The interface allows users to enter property characteristics and obtain
a predicted property price.

------------------------------------------------------------------------

# Features

-   End-to-end machine learning workflow
-   Separate models for houses and apartments
-   Data preparation notebooks
-   Model training notebooks
-   Flask web interface for prediction testing

------------------------------------------------------------------------

# Repository Structure

    dataset_raw/        Raw downloaded datasets
    datasets_prepd/     Cleaned and prepared datasets
    data_apt/           Apartment training data
    data_maison/        House training data
    models/             Trained machine learning models
    tmp_downloads/      Temporary downloaded archives
    templates/          html for the flask app

    download_data.py    Dataset download script
    prep_data.ipynb     Data preparation notebook
    train_apt.ipynb     Apartment model training
    train_maison.ipynb  House model training
    app.py              Flask prediction interface

------------------------------------------------------------------------