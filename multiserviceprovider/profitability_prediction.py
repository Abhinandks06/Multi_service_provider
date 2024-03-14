import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv("combined_data.csv")

X = df[['income', 'expense']]
y = df['is_profitable']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_train_scaled[['income', 'expense']] = scaler.fit_transform(X_train_scaled[['income', 'expense']])

X_test_scaled = X_test.copy()
X_test_scaled[['income', 'expense']] = scaler.transform(X_test_scaled[['income', 'expense']])

dt_model = DecisionTreeClassifier()
dt_model.fit(X_train_scaled, y_train)
dt_predictions = dt_model.predict(X_test_scaled)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
lr_predictions = lr_model.predict(X_test_scaled)

models = {'Decision Tree': dt_predictions, 'Logistic Regression': lr_predictions}

for model_name, predictions in models.items():
    accuracy = accuracy_score(y_test, predictions)
    print(f'{model_name} Accuracy: {accuracy}')
    conf_matrix = confusion_matrix(y_test, predictions)
    print(f'{model_name} Confusion Matrix:\n{conf_matrix}')
    print(f'{model_name} Classification Report:\n{classification_report(y_test, predictions)}')
    print('-' * 50)

new_data = pd.DataFrame({
    'income': [500000],
    'expense': [1000]
})
new_data_scaled = new_data.copy()
new_data_scaled[['income', 'expense']] = scaler.transform(new_data_scaled[['income', 'expense']])

dt_prediction = dt_model.predict(new_data_scaled)
lr_probabilities = lr_model.predict(new_data_scaled)

if dt_prediction[0] == 1:
    print('Decision Tree Prediction: The branch is profitable.')
else:
    print('Decision Tree Prediction: The branch is not profitable.')

if lr_probabilities[0] == 1:
    print(f'Logistic Regression Prediction: The branch is profitable.')
else:
    print(f'Logistic Regression Prediction: The branch is not profitable.')
