import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, r2_score
import seaborn as sns
import matplotlib.pyplot as plt

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


# Calculate accuracy and R2 score for Decision Tree
dt_accuracy = accuracy_score(y_test, dt_predictions)
dt_r2 = r2_score(y_test, dt_predictions)


# Display metrics for Decision Tree
print('Decision Tree:')
print(f'Accuracy: {dt_accuracy}')
print(f'R2 Score: {dt_r2}')
print(confusion_matrix(y_test, dt_predictions))
print(classification_report(y_test, dt_predictions))



# Visualize confusion matrices
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.heatmap(confusion_matrix(y_test, dt_predictions), annot=True, cmap='Blues', fmt='g')
plt.title('Decision Tree Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')


plt.tight_layout()
plt.show()

# Example prediction for new data
new_data = pd.DataFrame({
    'income': [1000],
    'expense': [25000],
    'number_of_workers': [5]
})
new_data_scaled = scaler.transform(new_data)

dt_prediction = dt_model.predict(new_data_scaled)


print("\nPredictions for new data:")
print(f'Decision Tree Prediction: {dt_prediction[0]}')


# Calculate target for new data
new_data_expense = new_data['expense'].iloc[0]
new_data_workers = new_data['number_of_workers'].iloc[0]
new_data_target = new_data_expense + ((new_data_expense) * (0.05 + (new_data_workers * 0.01)))

print(f'Target for new data: {new_data_target}')

if dt_prediction[0] == 1:
    print('Decision Tree Prediction: The branch is profitable.')
else:
    print('Decision Tree Prediction: The branch is not profitable.')



# Save the models
joblib.dump(dt_model, 'decision_tree_model.pkl')

