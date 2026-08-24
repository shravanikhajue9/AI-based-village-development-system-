# # import pandas as pd
# # import joblib

# # from sklearn.ensemble import RandomForestRegressor
# # from sklearn.model_selection import train_test_split
# # from sklearn.preprocessing import LabelEncoder

# # # Load Dataset
# # df = pd.read_csv(r"C:\Users\Saba\OneDrive\Documents\Aheri_Taluka_Smart_Village_Dataset_for_project.csv")
# # df.columns = df.columns.str.strip()

# # print(df.columns.tolist())


# # # Fill missing values instead of deleting rows
# # print("Rows:", len(df))
# # print(df.head())

# # # Separate numeric and non-numeric columns
# # num_cols = df.select_dtypes(include=['number']).columns
# # cat_cols = df.select_dtypes(exclude=['number']).columns

# # # Fill numeric columns with median
# # for col in num_cols:
# #     df[col] = df[col].fillna(df[col].median())

# # # Fill categorical columns with mode or "Unknown"
# # for col in cat_cols:
# #     df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
# # # Convert text columns into numbers
# # label_encoders = {}

# # for col in df.columns:

# #     if df[col].dtype == "object":

# #         le = LabelEncoder()

# #         df[col] = le.fit_transform(df[col].astype(str))

# #         label_encoders[col] = le


# # # Target Column
# # target = "Future Development Score"
# # print("Target exists:", target in df.columns)

# # X = df.drop(columns=[target])

# # y = df[target]

# # # Split
# # X_train, X_test, y_train, y_test = train_test_split(
# #     X,
# #     y,
# #     test_size=0.2,
# #     random_state=42
# # )

# # # Train Model
# # model = RandomForestRegressor(
# #     n_estimators=300,
# #     random_state=42
# # )
# # import pandas as pd
# # import joblib

# # from sklearn.ensemble import RandomForestRegressor
# # from sklearn.model_selection import train_test_split
# # from sklearn.preprocessing import LabelEncoder

# # # ==========================
# # # LOAD DATASET
# # # ==========================

# # df = pd.read_csv(
# #     r"C:\Users\Saba\OneDrive\Documents\Aheri_Taluka_Smart_Village_Dataset_for_project.csv"
# # )

# # df.columns = df.columns.str.strip()

# # # ==========================
# # # FILL MISSING VALUES
# # # ==========================

# # num_cols = df.select_dtypes(include=["number"]).columns
# # cat_cols = df.select_dtypes(exclude=["number"]).columns

# # for col in num_cols:
# #     df[col] = df[col].fillna(df[col].median())

# # for col in cat_cols:
# #     df[col] = df[col].fillna(df[col].mode()[0])

# # # ==========================
# # # LABEL ENCODING
# # # ==========================

# # label_encoders = {}

# # for col in cat_cols:

# #     le = LabelEncoder()

# #     df[col] = le.fit_transform(df[col].astype(str))

# #     label_encoders[col] = le

# # # ==========================
# # # TARGET
# # # ==========================

# # target = "Future Development Score"

# # X = df.drop(columns=[target])

# # y = df[target]

# # feature_columns = X.columns.tolist()

# # # ==========================
# # # TRAIN TEST SPLIT
# # # ==========================

# # X_train, X_test, y_train, y_test = train_test_split(
# #     X,
# #     y,
# #     test_size=0.2,
# #     random_state=42
# # )

# # # ==========================
# # # MODEL
# # # ==========================

# # model = RandomForestRegressor(
# #     n_estimators=300,
# #     random_state=42
# # )

# # model.fit(X_train, y_train)

# # # ==========================
# # # SAVE FILES
# # # ==========================

# # joblib.dump(model, "model.pkl")

# # joblib.dump(label_encoders, "label_encoders.pkl")

# # joblib.dump(feature_columns, "feature_columns.pkl")

# # print("===================================")
# # print("MODEL TRAINED SUCCESSFULLY")
# # print("===================================")
# # print("Files Created:")
# # print("✔ model.pkl")
# # print("✔ label_encoders.pkl")
# # print("✔ feature_columns.pkl")
# import pandas as pd
# import joblib

# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor

# # ==========================
# # LOAD DATASET
# # ==========================

# df = pd.read_csv(
#     r"C:\Users\Saba\OneDrive\Documents\Aheri_Taluka_Smart_Village_Dataset_for_project.csv"
# )

# df.columns = df.columns.str.strip()

# # ==========================
# # USE ONLY REQUIRED COLUMNS
# # ==========================

# X = df[
#     [
#         "Population",
#         "Literacy Rate (%)",
#         "Rainfall (mm)",
#         "Number of Schools",
#         "Number of Healthcare Centers",
#         "Unemployment Rate (%)"
#     ]
# ]

# y = df["Future Development Score"]

# # Missing values

# X = X.fillna(X.median())

# y = y.fillna(y.median())

# # ==========================
# # TRAIN TEST SPLIT
# # ==========================

# X_train, X_test, y_train, y_test = train_test_split(
#     X,
#     y,
#     test_size=0.2,
#     random_state=42
# )

# # ==========================
# # MODEL
# # ==========================

# model = RandomForestRegressor(
#     n_estimators=300,
#     random_state=42
# )

# model.fit(X_train, y_train)

# # ==========================
# # SAVE
# # ==========================

# joblib.dump(model, "model.pkl")
# joblib.dump(X.columns.tolist(), "feature_columns.pkl")

# print("================================")
# print("MODEL TRAINED SUCCESSFULLY")
# print("================================")

# print("Features Used:")

# print(X.columns.tolist())
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv(
    r"C:\Users\Saba\OneDrive\Documents\Aheri_Taluka_Smart_Village_Dataset_for_project.csv"
)

df.columns = df.columns.str.strip()

print("="*60)
print("DATASET INFORMATION")
print("="*60)

print(df.head())
print(df.info())
print(df.describe())

# =====================================
# MISSING VALUES
# =====================================

print("\nMissing Values:\n")
print(df.isnull().sum())

# Fill missing values

numeric_cols = df.select_dtypes(include=np.number).columns

df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# =====================================
# DUPLICATE VALUES
# =====================================

duplicates = df.duplicated().sum()

print("\nDuplicate Rows :", duplicates)

# Remove duplicates

df = df.drop_duplicates()

# =====================================
# OUTLIER DETECTION (IQR METHOD)
# =====================================

print("\nOutlier Detection\n")

for col in numeric_cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    print(col, ":", len(outliers))

# =====================================
# BOX PLOTS
# =====================================

for col in numeric_cols:

    plt.figure(figsize=(6,4))
    sns.boxplot(x=df[col])

    plt.title(f"Box Plot - {col}")

    plt.show()

# =====================================
# CORRELATION HEATMAP
# =====================================

plt.figure(figsize=(10,8))

corr = df[numeric_cols].corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.show()

# =====================================
# EXPLORATORY DATA ANALYSIS (EDA)
# =====================================

for col in numeric_cols:

    plt.figure(figsize=(6,4))

    sns.histplot(df[col], kde=True)

    plt.title(col)

    plt.show()

# Pairplot

sns.pairplot(df[numeric_cols])

plt.show()

# =====================================
# FEATURES
# =====================================

X = df[
    [
        "Population",
        "Literacy Rate (%)",
        "Rainfall (mm)",
        "Number of Schools",
        "Number of Healthcare Centers",
        "Unemployment Rate (%)"
    ]
]

y = df["Future Development Score"]

# =====================================
# FEATURE SELECTION
# =====================================

selector = SelectKBest(
    score_func=f_regression,
    k="all"
)

selector.fit(X, y)

feature_scores = pd.DataFrame({
    "Feature": X.columns,
    "Score": selector.scores_
})

feature_scores = feature_scores.sort_values(
    by="Score",
    ascending=False
)

print("\nFeature Selection Scores\n")
print(feature_scores)

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# MODEL
# =====================================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

# =====================================
# SAVE MODEL
# =====================================

joblib.dump(model, "model.pkl")
joblib.dump(X.columns.tolist(), "feature_columns.pkl")

print("\n================================")
print("MODEL TRAINED SUCCESSFULLY")
print("================================")

print("\nFeatures Used:")

print(X.columns.tolist())