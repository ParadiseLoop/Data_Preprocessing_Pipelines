# -*- coding: utf-8 -*-
"""Data_Preprocessing_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gU9WdlktgNRAuPGmhEYwXzfTWRgBVoIH

#**Data Pre-Processing Project**

The project focuses on the development of 3 distinct pipelines to process a starting dataset in order to put into practice what I've learnt during the corresponding course at Profession AI Master's in Data Engineering

Author: Daniel Aldehneh

## Importing Libraries and Data
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.decomposition import PCA
from sklearn.preprocessing import PowerTransformer, MinMaxScaler
import numpy as np
import joblib

import pandas as pd

url = "https://raw.githubusercontent.com/ParadiseLoop/Data_Preprocessing_Pipelines/main/data.csv"
df = pd.read_csv(url, sep = ";", header=1)

df.head()

df=df.drop(columns="Unnamed: 0")

"""## Pipeline 1: Pre-Processing when Target = 1

This pipeline focuses on pre-processing only the records where the **target is equal to 1**, meaning the positive cases of tumor detection. The pipeline includes:

- **Missing Value Cleaning**: The cleaning process will differ between symmetric and asymmetric variables. For asymmetric variables, imputation techniques that consider the data distribution will be used, while more standard imputation methods will be applied to symmetric variables.

- **Symmetrization of Asymmetric Variables**: To ensure a more balanced distribution of the data, the values of asymmetric variables will be adjusted using symmetrization techniques.

- **One-Hot Encoding for Categorical Variables**: All categorical variables will be converted into a numerical format using one-hot encoding, making the data suitable for machine learning models.

- **Rescaling through Standardization**: Numeric variables will be scaled using standardization to ensure that all variables have a distribution with a mean of zero and a standard deviation of one.

Let us start by filtering the dataset for rows where target = 1
"""

df1=df.copy()
y1 = df1[df1["target"]==1]

y1.head()

y1.dtypes

y1['area error'].unique()

y1_float = y1.select_dtypes(include=['float64'])

for column in y1_float.columns:
  plt.figure(figsize=(10,5))
  plt.hist(y1_float[column], color="blue")
  plt.title(f"{column} variable distribution")
  plt.xlabel(y1_float[column])
  plt.ylabel("Frequency")
  plt.show()

y1_ws_analysis=y1_float[y1_float["worst symmetry"]<50]
y1_ws_analysis2=y1_float[y1_float["worst symmetry"]>50]

plt.figure(figsize=(10,5))
  plt.hist(y1_ws_analysis["worst symmetry"],bins=20, color="blue")
  plt.title(f"worst symmetry variable distribution")
  plt.xlabel(y1_float[column])
  plt.ylabel("Frequency")
  plt.show()

plt.figure(figsize=(10,5))
  plt.hist(y1_ws_analysis2["worst symmetry"],bins=20, color="blue")
  plt.title(f"worst symmetry variable distribution")
  plt.xlabel(y1_float[column])
  plt.ylabel("Frequency")
  plt.show()

skewness = y1_float.skew()

symmetric= skewness[abs(skewness) < 1].index.tolist()
asymmetric= skewness[abs(skewness) > 1].index.tolist()
categorical = ["area error"]

ct = ColumnTransformer([
    (
        'symmetrical', Pipeline([

        ('imputer', SimpleImputer(strategy='most_frequent')),
         ('scaler', StandardScaler())
         ]),symmetric),

    (
        'asymmetrical', Pipeline([

        ('imputer', SimpleImputer(strategy='most_frequent')),
         ('power',PowerTransformer()),
         ('scaler', StandardScaler())
         ]),asymmetric),
    (
        ('categorical', Pipeline([
        ('imputer', SimpleImputer(strategy='constant',fill_value="N")),
         ('onehot', OneHotEncoder())
         ]),categorical))
    ], remainder='passthrough' ,verbose_feature_names_out=False)

ct.fit(y1)

transformed_y1=ct.transform(y1)

feature_names = ct.get_feature_names_out()
transformed_y1 = pd.DataFrame(transformed_y1, columns=feature_names, index=y1.index)

transformed_y1.head()

"""let's plug the y = 1 rows back into the original dataframe"""

transformed_y1.index = y1.index
df1.loc[df1["target"]==1, transformed_y1.columns] = transformed_y1

"""### Pipeline's effect - Comparison with original data

**Summary**
"""

print("Original Dataframe (df) Summary Statistics:")
print(df.describe())

print("\nTransformed Dataframe (df1) Summary Statistics:")
print(df1.describe())

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

print("Original Skewness (df):")
print(df[numeric_cols].skew())

print("\nTransformed Skewness (df1):")
print(df1[numeric_cols].skew())

"""## Pipeline 2: Pre-Processing with binning and encoding on all records

This pipeline will be applied to all records in the dataset, with the goal of transforming all numerical and categorical variables through the following stages:

* **Missing Values Cleaning**: A customized strategy will be adopted to fill in missing values consistently with the nature of the variables.

* **Discretization of Numerical Variables into 20 Bins**: Numerical variables will be discretized into 20 bins to reduce data complexity and facilitate analysis.
* **Ordinal Encoding of Categorical Variables**: Categorical variables will be encoded based on an ascending order (A, B, C), preserving the semantic meaning of the values.
* **Selection of the 5 Most Informative Variables**: After the transformations, the five most informative variables relative to the target will be selected using an appropriate metric, thereby improving the efficiency and accuracy of subsequent models.




"""

df2=df.copy()

ct = ColumnTransformer([
    (
        'numericals',
        Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('discretizer', KBinsDiscretizer(n_bins=20, encode='ordinal', strategy='uniform'))

        ]),
        make_column_selector(dtype_exclude='object')
    ),
    (
        "chars",
        Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='N')),
            ('ordinal', OrdinalEncoder())
        ]),
        make_column_selector(dtype_include='object')
    )

])

feature_selector2 = SelectKBest(f_classif,k = 5)

pipeline2 = Pipeline([
    ('preprocessing', ct),
    ('selector', feature_selector2)
])

X = df2.drop('target',axis=1)
y = df2['target']

pipeline2.fit(X,y)

transformed_df2=pipeline2.transform(df2)

"""Let's check out the most informative variables"""

feature_names = pipeline2.get_feature_names_out()
transformed_df2 = pd.DataFrame(transformed_df2, columns=feature_names, index=df2.index)

transformed_df2.head()

"""## Pipeline 3: Pre-Processing of numerical variables

This pipeline focuses exclusively on numerical variables, applying advanced transformation techniques:

- **Missing Values Cleaning**: as in the previous pipeline, an appropriate cleaning method will be chosen for the numerical variables.

- **Principal Component Analysis (PCA)**: PCA will be applied to reduce the dimensionality of the dataset while retaining **80% of the explained variance**. This will help reduce noise and improve model performance.

- **Symmetrization**: as in Pipeline 1, asymmetric variables will be symmetrized here as well to improve their distribution.

- **Rescaling through Normalization**: finally, the numerical variables will be normalized **between 0 and 1**, to standardize the scale and facilitate the learning process of the models.


"""

df3 = df.copy()

num_cols = df3.select_dtypes(include=[np.number]).columns

ct3 = ColumnTransformer([
    (
        'numeriche',
      Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('pca', PCA(n_components=0.80, svd_solver='full')),
    ('symmetrizer', PowerTransformer(method='yeo-johnson')),
    ('scaler', MinMaxScaler())
    ]),
        make_column_selector(dtype_exclude=['object','category','bool']))
])

ct3.fit(df3)

transformed_df3=ct3.transform(df3)

"""Let's check out the resulting DataFrame"""

feature_names = ct3.get_feature_names_out()
transformed_df3 = pd.DataFrame(transformed_df3, columns=feature_names, index=df3.index)

transformed_df3.head()

"""## Saving Pipelines for future use

Let's save the 3 pipelines we created for future use using the **joblib** library
"""

joblib.dump(ct, "ct.pkl")

joblib.dump(ct, "pipeline2.pkl")

joblib.dump(ct, "ct3.pkl")

"""I went on and saved the pipelines on Github at this link:

https://github.com/ParadiseLoop/Data_Preprocessing_Pipelines/tree/main/pipelines
"""