import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import VarianceThreshold


def load_and_preprocess(path="data/diabetes.csv"):
    # Define expected column names
    columns = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin",
               "BMI","DiabetesPedigreeFunction","Age","Outcome"]

    # Try reading dataset normally first
    df = pd.read_csv(path)

    # If headers are missing, assign column names manually
    if list(df.columns) != columns:
        df = pd.read_csv(path, names=columns, header=None)

    # Replace invalid 0s with NaN
    cols_with_invalid_zeros = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    df[cols_with_invalid_zeros] = df[cols_with_invalid_zeros].replace(0, np.nan)

    # Impute missing values using median
    df[cols_with_invalid_zeros] = df[cols_with_invalid_zeros].fillna(df[cols_with_invalid_zeros].median())

    # Save cleaned dataset
    df.to_csv("data/pima_diabetes_cleaned.csv", index=False)

    # Separate features & labels
    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]

    # Min-Max Scaling → Keep as DataFrame to retain headers
    scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # After scaling
    selector = VarianceThreshold(threshold=0.01)  # remove features with very low variance
    X_scaled = pd.DataFrame(selector.fit_transform(X_scaled), columns=X.columns[selector.get_support()])

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, stratify=y, random_state=42
    )

    return X_train, X_test, y_train, y_test, scaler, X.columns
