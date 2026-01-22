import requests
import json
from django.conf import settings

# API Key provided by user
PLANTNET_API_KEY = "2b10NyH36sYkTs8MdZu6MrjAve"
API_ENDPOINT = "https://my-api.plantnet.org/v2/identify/all"

def identify_plant(image_path):
    """
    Gửi ảnh đến PlantNet API để nhận diện cây.
    
    Args:
        image_path (str): Đường dẫn tuyệt đối đến file ảnh.
        
    Returns:
        dict: Kết quả nhận diện tốt nhất hoặc None nếu lỗi.
              Format: {'name': 'Plant Name', 'score': 0.95, 'common_names': ['Name 1', 'Name 2']}
    """
    try:
        # Chuẩn bị parameters
        params = {
            "api-key": PLANTNET_API_KEY
        }
        
        # Chuẩn bị file
        files = {
            "images": open(image_path, "rb")
        }
        
        # Gửi request
        response = requests.post(API_ENDPOINT, params=params, files=files)
        
        # Kiểm tra status code
        if response.status_code == 200:
            data = response.json()
            
            # Lấy kết quả tốt nhất
            if 'results' in data and len(data['results']) > 0:
                best_match = data['results'][0]
                species = best_match['species']
                score = best_match['score']
                
                common_names = species.get('commonNames', [])
                scientific_name = species.get('scientificNameWithoutAuthor', 'Unknown')
                
                return {
                    'name': scientific_name,
                    'score': score * 100, # Chuyển sang phần trăm
                    'common_names': common_names,
                    'raw_data': json.dumps(best_match)
                }
        else:
            print(f"Error from PlantNet API: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception calling PlantNet API: {str(e)}")
        return None
    finally:
        # Đảm bảo đóng file nếu cần thiết (files dictionary open context)
        # requests mở file nhưng tốt nhất là quản lý resource, 
        # nhưng ở đây files=open(...) ngắn gọn, requests sẽ đọc, nhưng không auto close.
        # Python GC sẽ lo, hoặc dùng context manager. 
        pass
        
