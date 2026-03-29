"""
Debug v3: Check what INTENT the model predicts for 'giá cả cây kim tiền'.
Runs standalone using joblib to avoid Django hanging.
"""
import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), 'plant_recommendation', 'intent_model.pkl')
model = joblib.load(model_path)

test_queries = [
    "giá cả cây kim tiền",
    "giá cây kim tiền",
    "cây kim tiền",
    "cây sung",
    "giá cả cây sung",
    "tôi muốn mua cây kim tiền",
    "chào shop",
    "tư vấn cho mình với",
    "tìm cho tôi 4 cây ngoài trời",
    "tìm cho tôi 5 cây trong nhà",
    "cây dễ chăm",
    "tìm cho tôi cây dễ sống",
]

for q in test_queries:
    pred = model.predict([q])[0]
    proba = model.predict_proba([q])
    classes = model.classes_
    top = sorted(zip(classes, proba[0]), key=lambda x: -x[1])[:3]
    print(f"Input: {q!r}")
    print(f"  -> Intent: {pred}")
    print(f"  -> Top probs: {[(c, round(p, 3)) for c, p in top]}")
