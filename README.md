# Data Pre-Processing Project

This project focuses on the development of **three distinct data preprocessing pipelines** to transform a starting dataset, applying the techniques studied during the "Profession AI Master's in Data Engineering" course.

Author: **Daniel Aldehneh**

---

## Project Overview

The main goal of this project is to build reusable and modular preprocessing pipelines, following best practices in data science workflows.  
Each pipeline addresses different data transformation challenges, including missing value handling, feature engineering, and dimensionality reduction.

---

## Data Source

The dataset is publicly accessible via GitHub:  
[🔗 Link to dataset](https://raw.githubusercontent.com/ParadiseLoop/Data_Preprocessing_Pipelines/main/data.csv)

---

## Pipelines Description

### Pipeline 1: Pre-Processing when `target = 1`
- Filters only records where `target = 1` (positive cases).
- Cleans missing values differently based on feature distribution (symmetric/asymmetric).
- Symmetrizes asymmetric variables.
- Applies one-hot encoding to categorical features.
- Standardizes numerical features.

### Pipeline 2: Pre-Processing with Binning and Encoding (All Records)
- Handles missing values across all records.
- Discretizes numerical variables into 20 uniform bins.
- Applies ordinal encoding to categorical variables.
- Selects the 5 most informative features using `SelectKBest` with ANOVA F-value.

### Pipeline 3: Pre-Processing of Numerical Variables
- Focuses solely on numerical features.
- Cleans missing values with mean imputation.
- Applies PCA to retain 80% of variance.
- Symmetrizes using `PowerTransformer`.
- Normalizes features between 0 and 1.

---

## Saved Pipelines

The following pipelines were serialized with `joblib` and are available for reuse:

- `ct.pkl` → Preprocessing transformer from Pipeline 1
- `pipeline2.pkl` → Complete preprocessing and feature selection pipeline from Pipeline 2
- `ct3.pkl` → Preprocessing transformer from Pipeline 3

You can find them here:  
[🔗 Link to saved pipelines](https://github.com/ParadiseLoop/Data_Preprocessing_Pipelines/tree/main/pipelines)

---

## How to Use the Pipelines

To load a saved pipeline and apply it to new data:

```python
import joblib
import pandas as pd

# Example: Load pipeline 1
pipeline1 = joblib.load('pipelines/ct.pkl')

# Load new data
url = "https://raw.githubusercontent.com/ParadiseLoop/Data_Preprocessing_Pipelines/main/data.csv"
new_data = pd.read_csv(url, sep=";", header=1)
new_data = new_data.drop(columns="Unnamed: 0")

# Transform new data
transformed_data = pipeline1.transform(new_data)
