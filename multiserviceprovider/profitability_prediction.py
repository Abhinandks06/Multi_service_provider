import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, r2_score

# Load the dataset
df = pd.read_csv("combined_data.csv")

# Define features and target variable
X = df[['income', 'expense', 'number_of_workers']]
y = df['is_profitable']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Decision Tree model
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train_scaled, y_train)
dt_predictions = dt_model.predict(X_test_scaled)

# Train Random Forest model
rf_model = RandomForestClassifier() 
rf_model.fit(X_train_scaled, y_train)
rf_predictions = rf_model.predict(X_test_scaled)

# Models dictionary
models = {'Decision Tree': dt_predictions, 'Random Forest': rf_predictions}

# Evaluate models
for model_name, predictions in models.items():
    accuracy = accuracy_score(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f'{model_name} Accuracy: {accuracy}')
    print(f'{model_name} R2 Score: {r2}')
    conf_matrix = confusion_matrix(y_test, predictions)
    print(f'{model_name} Confusion Matrix:\n{conf_matrix}')
    print(f'{model_name} Classification Report:\n{classification_report(y_test, predictions)}')
    print('-' * 50)

# Example prediction for new data
new_data = pd.DataFrame({
    'income': [1000],
    'expense': [25000],
    'number_of_workers': [5]
})
new_data_scaled = scaler.transform(new_data)

dt_prediction = dt_model.predict(new_data_scaled)
rf_prediction = rf_model.predict(new_data_scaled)

print("Predictions for new data:")
print(f'Decision Tree Prediction: {dt_prediction[0]}')
print(f'Random Forest Prediction: {rf_prediction[0]}')

# Calculate target for new data
new_data_expense = new_data['expense'].iloc[0]
new_data_workers = new_data['number_of_workers'].iloc[0]
new_data_target = new_data_expense + ((new_data_expense) * (0.05 + (new_data_workers * 0.01)))

print(f'Target for new data: {new_data_target}')

if dt_prediction[0] == 1:
    print('Decision Tree Prediction: The branch is profitable.')
else:
    print('Decision Tree Prediction: The branch is not profitable.')

if rf_prediction[0] == 1:
    print(f'Random Forest Prediction: The branch is profitable.')
else:
    print(f'Random Forest Prediction: The branch is not profitable.')

# Save the models
joblib.dump(dt_model, 'decision_tree_model.pkl')
joblib.dump(rf_model, 'random_forest_model.pkl')
