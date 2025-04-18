# -*- coding: utf-8 -*-
"""Final models with all data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZHPebdqOGQ-EJRZiPzp4RrnDPYBVakwU

### Regression trees with all data
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt


file_path = '/content/all_data_stationary_growthratestransf_final1.csv'
df = pd.read_csv(file_path)


df['Start_date'] = pd.to_datetime(df['Start_date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
df.dropna(subset=['Start_date'], inplace=True)

df['day_of_week'] = df['day_of_week'].astype('category').cat.codes


y_col = 'growth_rates'
lag_cols = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'lag_6', 'lag_7', 'lag_8', 'lag_9', 'lag_10']
covariate_cols = ['Belgium_MWh', 'Denmark_1_MWh', 'Denmark_2_MWh', 'France_MWh',
                  'Netherlands_MWh', 'Norway_2_MWh', 'Austria_MWh', 'Poland_MWh', 'Sweden_4_MWh',
                  'Switzerland_MWh', 'Czech_Republic_MWh','Northern_Italy_MWh',
                  'Slovenia_MWh', 'Hungary_MWh', 'Biomass_MWh', 'Hydropower_MWh', 'Wind_offshore_MWh',
                  'Wind_onshore_MWh', 'Photovoltaics_MWh', 'Other_renewable_MWh', 'Nuclear_MWh',
                  'Lignite_MWh', 'Hard_coal_MWh', 'Fossil_gas_MWh', 'Hydro_pumped_storage_MWh',
                  'Other_conventional_MWh', 'Temperature_2m', 'Cloud_cover', 'Wind_speed_10m',
                  'Holiday_Dummy', 'hour_of_day', 'day_of_year' , 'day_of_week_sunday',
                  'day_of_week_saturday', 'day_of_week_monday','day_of_week']

df.dropna(subset=lag_cols + covariate_cols + [y_col], inplace=True)


X_lags = df[lag_cols].values
X_covariates = df[covariate_cols].values
X = np.hstack((X_lags, X_covariates))
y = df[y_col].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


tree_model = DecisionTreeRegressor(random_state=42, max_depth=6)
tree_model.fit(X_train, y_train)


n_test = len(X_test)
predictions_tree = np.zeros(n_test)
current_lags = X_test[0, :len(lag_cols)]

for i in range(n_test):
    new_data = np.hstack((current_lags, X_test[i, len(lag_cols):])).reshape(1, -1)
    prediction = tree_model.predict(new_data)[0]
    predictions_tree[i] = prediction
    current_lags = np.roll(current_lags, -1)
    current_lags[-1] = y_test[i]

"""### Plotting regression trees and its rmse"""

# RMSE Calculation
rmse_tree = np.sqrt(mean_squared_error(y_test, predictions_tree))
print(f"Regression Tree RMSE: {rmse_tree}")


plt.figure(figsize=(14, 7))
last_n = 199
plt.plot(df['Start_date'].iloc[-last_n:], y_test[-last_n:], label='Actual')
plt.plot(df['Start_date'].iloc[-last_n:], predictions_tree[-last_n:], label='Predicted (Regression Tree)', alpha=0.6)
plt.title('Actual vs Predicted Growth Rates (Regression Tree)')
plt.xlabel('Date')
plt.ylabel('Growth Rates')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""### Random forest with all data"""

from sklearn.ensemble import RandomForestRegressor

# Random Forest Model
forest_model = RandomForestRegressor(n_estimators=1000, random_state=42)
forest_model.fit(X_train, y_train)

# Iterative Forecasting
predictions_rf = np.zeros(n_test)
current_lags = X_test[0, :len(lag_cols)]

for i in range(n_test):
    new_data = np.hstack((current_lags, X_test[i, len(lag_cols):])).reshape(1, -1)
    predictions_rf[i] = forest_model.predict(new_data)[0]
    current_lags = np.roll(current_lags, -1)
    current_lags[-1] = y_test[i]


rmse_rf = np.sqrt(mean_squared_error(y_test, predictions_rf))
print(f"Random Forest RMSE: {rmse_rf}")


plt.figure(figsize=(14, 7))
last_n = 399
plt.plot(df['Start_date'].iloc[-last_n:], y_test[-last_n:], label='Actual')
plt.plot(df['Start_date'].iloc[-last_n:], predictions_rf[-last_n:], label='Predicted (Random Forest)', alpha=0.6)
plt.title('Actual vs Predicted Growth Rates (Random Forest)')
plt.xlabel('Date')
plt.ylabel('Growth Rates')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""### Plotting random forests and its *rmse*"""

rmse_rf = np.sqrt(mean_squared_error(y_test, predictions_rf))
print(f"Random Forest RMSE: {rmse_rf}")

plt.figure(figsize=(14, 7))
last_n = 499
plt.plot(df['Start_date'].iloc[-last_n:], y_test[-last_n:], label='Actual')
plt.plot(df['Start_date'].iloc[-last_n:], predictions_rf[-last_n:], label='Predicted (Random Forest)', alpha=0.6)
plt.title('Actual vs Predicted Growth Rates (Random Forest)')
plt.xlabel('Date')
plt.ylabel('Growth Rates')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""### Feature importance for both models"""

tree_feature_importances = tree_model.feature_importances_

print("Decision Tree Feature Importances:")
for i, col in enumerate(lag_cols + covariate_cols):
    print(f"{col}: {tree_feature_importances[i]}")

forest_feature_importances = forest_model.feature_importances_

print("\nRandom Forest Feature Importances:")
for i, col in enumerate(lag_cols + covariate_cols):
    print(f"{col}: {forest_feature_importances[i]}")

"""### Computing the permutations of feature importance for regression trees"""

feature_names = lag_cols + covariate_cols

X_lags = df[lag_cols].values
X_covariates = df[covariate_cols].values
X = np.hstack((X_lags, X_covariates))
y = df[y_col].values

#(70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)





from sklearn.inspection import permutation_importance

result_tree = permutation_importance(tree_model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1)

perm_importances_tree = pd.DataFrame({
    'Feature': feature_names,
    'Importance Mean': result_tree.importances_mean,
    'Importance Std': result_tree.importances_std
})

print(perm_importances_tree)
perm_importances_tree.to_csv('decision_tree_permutation_importances.csv', index=False)

"""### Computing the permutations of feature importance for random forests"""

result_rf = permutation_importance(forest_model, X_test, y_test, n_repeats=5, random_state=42, n_jobs=-1)

perm_importances_rf = pd.DataFrame({
    'Feature': feature_names,
    'Importance Mean': result_rf.importances_mean,
    'Importance Std': result_rf.importances_std
})
perm_importances_rf.to_csv('random_forest_permutation_importances.csv', index=False)

