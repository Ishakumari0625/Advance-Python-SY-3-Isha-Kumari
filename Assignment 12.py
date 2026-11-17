import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create customer churn dataset
data = {
    "CustomerID": range(1, 11),
    "Gender": ["Male", "Female", "Male", "Female", "Male",
               "Female", "Male", "Female", "Male", "Female"],
    "Age": [25, 32, 45, 28, 51, 36, 42, 29, 55, 31],
    "Tenure": [2, 5, 8, 1, 10, 4, 7, 2, 12, 3],
    "MonthlyCharges": [50, 70, 90, 45, 100, 65, 85, 55, 110, 60],
    "TotalCharges": [100, 350, 720, 45, 1000, 260, 595, 110, 1320, 180],
    "Churn": ["Yes", "No", "No", "Yes", "No",
              "Yes", "No", "Yes", "No", "Yes"]
}

df = pd.DataFrame(data)

# Display first 5 rows
print("First 5 rows:")
print(df.head())

# Dataset information
print("\nDataset Information:")
df.info()

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Churn count
print("\nChurn Distribution:")
print(df["Churn"].value_counts())

# Churn percentage
print("\nChurn Percentage:")
print(df["Churn"].value_counts(normalize=True) * 100)

# Churn visualization
df["Churn"].value_counts().plot(kind="bar")

plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")
plt.show()

# Age distribution
df["Age"].plot(kind="hist", bins=5)

plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Customers")
plt.show()

# Churn by Gender
pd.crosstab(df["Gender"], df["Churn"]).plot(kind="bar")

plt.title("Churn by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Customers")
plt.show()

# Correlation matrix
print("\nCorrelation Matrix:")
print(df.select_dtypes(include=np.number).corr())