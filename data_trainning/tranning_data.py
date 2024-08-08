# Import the library
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
# import time
import joblib
import numpy as np

# Start the timer
# start_time = time.time()
# Load the data
df = pd.read_csv('../data_gen/water_level_data.csv')

# Splitting the data
X = df[['Water Level (m)']]  # Ensure X is a DataFrame, not a Series
y = df['Flood Occurrence']

# Split the data with a fixed random_state for reproducibility
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

#Save the model in joblib
joblib.dump(model, 'trained_model.joblib')

#Make predictions
y_pred = model.predict(X_test)

# cm = confusion_matrix(y_test, y_pred)
#
# plt.figure(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No Flood', 'Flood'], yticklabels=['No Flood', 'Flood'])
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.title('Confusion Matrix')
# plt.show()

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
# Predict probabilities
X_values = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
y_proba = model.predict_proba(X_values)[:, 1]

# Find the water level corresponding to 50% probability
threshold = 0.5
threshold_index = np.where(np.abs(y_proba - threshold) == np.min(np.abs(y_proba - threshold)))[0][0]
threshold_water_level = X_values[threshold_index][0]

# Plot the data and the logistic regression curve
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='red', label='Data Points')
plt.plot(X_values, y_proba, color='blue', label='Logistic Regression Curve')
plt.axhline(y=0.5, color='green', linestyle='--', label='50% Threshold')
plt.axvline(x=threshold_water_level, color='orange', linestyle='--', label=f'Threshold Water Level: {threshold_water_level:.2f}m')
plt.xlabel('Water Level (m)')
plt.ylabel('Flood Occurrence Probability')
plt.title('Logistic Regression with S-Curve and 50% Threshold')
plt.legend()
plt.show()

# # End the timer
# end_time = time.time()
#
# # Calculate the elapsed time
# elapsed_time = end_time - start_time
#
# print(f"Elapsed time: {elapsed_time:.2f} seconds")
