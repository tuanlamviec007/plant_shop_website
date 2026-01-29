import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# 1. Load Data
df = pd.read_csv('plants_10_limited.csv')
print("Dataset samples:")
print(df.head())

# 2. Features & Target
X = df[['light', 'location', 'care']]
y = df['name']

# 3. Encoding (Chuyển chữ thành số)
le_light = LabelEncoder()
le_location = LabelEncoder()
le_care = LabelEncoder()
le_name = LabelEncoder()

X['light'] = le_light.fit_transform(X['light'])
X['location'] = le_location.fit_transform(X['location'])
X['care'] = le_care.fit_transform(X['care'])
y_encoded = le_name.fit_transform(y)

print("\nEncoding mapping:")
print(f"Light: {dict(zip(le_light.classes_, le_light.transform(le_light.classes_)))}")
print(f"Location: {dict(zip(le_location.classes_, le_location.transform(le_location.classes_)))}")
print(f"Care: {dict(zip(le_care.classes_, le_care.transform(le_care.classes_)))}")

# 4. Train Model
clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf.fit(X, y_encoded)

# 5. Save Model & Encoders
model_dir = 'plant_recommendation/ml_models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

joblib.dump(clf, f'{model_dir}/decision_tree_model.pkl')
joblib.dump(le_light, f'{model_dir}/le_light.pkl')
joblib.dump(le_location, f'{model_dir}/le_location.pkl')
joblib.dump(le_care, f'{model_dir}/le_care.pkl')
joblib.dump(le_name, f'{model_dir}/le_name.pkl')

print(f"\n✅ Model saved to {model_dir}/")

# 6. Test Prediction (Example)
# Input: Light=low, Location=indoor, Care=low -> Expect Lưỡi Hổ / Kim Ngân...
test_input = pd.DataFrame({
    'light': [le_light.transform(['low'])[0]],
    'location': [le_location.transform(['indoor'])[0]],
    'care': [le_care.transform(['low'])[0]]
})
pred_id = clf.predict(test_input)[0]
pred_name = le_name.inverse_transform([pred_id])[0]
print(f"\nTest Prediction for (Low, Indoor, Low): {pred_name}")
