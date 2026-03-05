import requests

url = "http://127.0.0.1:8000/ai-recognition/chat-api/"
headers = {"Content-Type": "application/json"}
data = {"message": "tôi muốn tìm cây đào"}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    try:
        json_data = response.json()
        print("Response JSON:")
        print(json_data)
        if "data" in json_data:
            print(f"Number of Products: {len(json_data['data'])}")
    except Exception as e:
        print("Response text:", response.text)
except Exception as e:
    print("Error:", str(e))
