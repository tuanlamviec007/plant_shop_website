import os
import json
import joblib
import underthesea
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

script_dir = os.path.dirname(os.path.abspath(__file__))

def load_data():
    file_path = os.path.join(script_dir, "training_data.json")
    if not os.path.exists(file_path):
        print("Không tìm thấy training_data.json. Vui lòng chạy generate_data.py trước!")
        return None, None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    texts = []
    labels = []
    
    for item in data:
        texts.append(item["text"])
        labels.append(item["intent"])
        
    return texts, labels

import sys
# Ensure absolute imports for Django compatibility if needed
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from plant_recommendation.ai_service import _normalize_text

def preprocess_text(text):
    # Tiền xử lý: Dùng underthesea để word_tokenize, kèm theo normalize của hệ thống
    try:
        norm = _normalize_text(text)
        tokenized = underthesea.word_tokenize(norm, format="text")
        return tokenized
    except Exception as e:
        return _normalize_text(text) # Fallback

def train_intent_model():
    print("Đang đọc dữ liệu huấn luyện...")
    texts, labels = load_data()
    if not texts:
        return
        
    print(f"Tổng số mẫu: {len(texts)}")
    
    # Tiền xử lý
    print("Đang tiền xử lý văn bản (Word Tokenization)...")
    processed_texts = [preprocess_text(t) for t in texts]
    
    # Do số lượng data ít, ta có thể chỉ chia train/test đơn giản hoặc train trên toàn bộ
    # Ở đây do tập mẫu chỉ ~70-80 câu nên train trên toàn bộ tập để model nhạy nhất
    X_train = processed_texts
    y_train = labels

    print("Đang khởi tạo mô hình học máy (TF-IDF + LogisticRegression)...")
    # Sử dụng Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))), # 1-gram và 2-gram
        ('clf', LogisticRegression(C=1.0, class_weight='balanced', solver='lbfgs', random_state=42))
    ])

    print("Đang tiến hành huấn luyện (Training)...")
    pipeline.fit(X_train, y_train)

    # Đánh giá nhanh trên chính tập train (để check overfit hi vọng gần 100%)
    y_pred = pipeline.predict(X_train)
    print("\n--- KẾT QUẢ ĐÁNH GIÁ TRÊN TẬP HUẤN LUYỆN ---")
    print(classification_report(y_train, y_pred))

    # Lưu model
    model_path = os.path.join(script_dir, "intent_model.pkl")
    joblib.dump(pipeline, model_path)
    print(f"Đã lưu mô hình tại: {model_path}")
    print("Hoàn tất quy trình huấn luyện!")

if __name__ == "__main__":
    train_intent_model()
