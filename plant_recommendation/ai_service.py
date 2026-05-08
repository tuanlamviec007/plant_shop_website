import os
import json
import google.generativeai as genai
from django.conf import settings
from products.models import Product

def _load_plants():
    # Đọc thông tin phong thủy/chăm sóc từ JSON
    plants_path = os.path.join(settings.BASE_DIR, 'plant_recommendation', 'selected_plants.json')
    try:
        with open(plants_path, 'r', encoding='utf-8-sig') as f:
            json_plants = json.load(f)
    except Exception:
        json_plants = []
        
    json_plants_dict = {p['id']: p for p in json_plants}
    
    # Ghép với thông tin Giá tiền từ Database thật
    plants_data = []
    db_products = Product.objects.filter(is_active=True)
    for p in db_products:
        info = {
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price),
        }
        # Nếu có thông tin bổ sung từ JSON thì thêm vào
        if p.id in json_plants_dict:
            info['characteristics'] = json_plants_dict[p.id].get('characteristics', '')
            info['meaning'] = json_plants_dict[p.id].get('meaning', '')
            info['care'] = json_plants_dict[p.id].get('care', '')
        plants_data.append(info)
        
    return plants_data

def _build_context(plants):
    context_str = "Dưới đây là danh sách CÂY DUY NHẤT mà bạn được phép tư vấn và bán tại Green Plant Shop:\n\n"
    for p in plants:
        # Fomat giá tiền kiểu Việt Nam (VD: 150,000 đ)
        formatted_price = f"{int(p['price']):,} đ"
        context_str += f"- Tên: {p['name']} (ID: {p['id']}, Giá tiền: {formatted_price})\n"
        if p.get('characteristics'): context_str += f"  Đặc điểm: {p['characteristics']}\n"
        if p.get('care'): context_str += f"  Cách chăm sóc: {p['care']}\n"
        if p.get('meaning'): context_str += f"  Ý nghĩa phong thủy: {p['meaning']}\n"
        context_str += "\n"
    return context_str

def chatbot_response(request_message, chat_history):
    # Cấu hình Gemini
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        return {
            'message': "Hệ thống chưa được cấu hình API Key. Vui lòng liên hệ quản trị viên.",
            'data': [],
            'suggested_replies': [],
            'updated_history': chat_history
        }
        
    genai.configure(api_key=api_key)
    
    plants = _load_plants()
    plant_context = _build_context(plants)
    
    system_prompt = f"""Bạn là trợ lý ảo tư vấn cây cảnh vô cùng thân thiện, chuyên nghiệp của Green Plant Shop.

{plant_context}

NHIỆM VỤ CỦA BẠN:
1. Tư vấn các loại cây phù hợp với nhu cầu, sở thích, không gian hoặc phong thủy của người dùng.
2. Hướng dẫn cách chăm sóc cây.
3. Luôn trả lời bằng TIẾNG VIỆT tự nhiên, dùng emoji phù hợp.
4. NẾU KHÁCH HỎI CÂY KHÔNG CÓ TRONG DANH SÁCH TRÊN: Hãy nói xin lỗi một cách khéo léo rằng shop hiện không có loại cây đó, và chủ động gợi ý một số cây khác có đặc tính tương tự trong danh sách.
5. Định dạng văn bản bằng Markdown (in đậm `**text**`, bullet points `- item`) để dễ đọc.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (STRICT JSON):
Bạn PHẢI trả về ĐÚNG MỘT OBJECT JSON hợp lệ, KHÔNG có markdown code block, KHÔNG có text thừa.
Cấu trúc JSON:
{{
  "message": "Câu trả lời của bạn, định dạng Markdown",
  "suggested_product_ids": [id_1, id_2], // Chỉ dùng ID số nguyên từ danh sách trên nếu bạn muốn gợi ý cây. Array rỗng [] nếu không có. Tối đa 4 ID.
  "suggested_replies": ["Gợi ý 1", "Gợi ý 2", "Gợi ý 3"] // 2-3 câu hỏi gợi ý tiếp theo cho khách hàng (ngắn gọn dưới 10 chữ).
}}
"""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=system_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Chuyển đổi lịch sử chat cho Gemini
        gemini_history = []
        for h in chat_history:
            role = "user" if h["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [h["text"]]})
            
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(request_message)
        
        # Parse kết quả JSON
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            print("Failed to decode JSON from Gemini:", response.text)
            result = {
                "message": response.text, 
                "suggested_product_ids": [], 
                "suggested_replies": ["Bắt đầu lại", "Xem tất cả cây"]
            }
            
        # Cập nhật lịch sử
        updated_history = chat_history + [
            {"role": "user", "text": request_message},
            {"role": "bot", "text": response.text}
        ]
        updated_history = updated_history[-10:] # Giữ 10 tin nhắn gần nhất
        
        # Lấy thông tin sản phẩm từ Database
        response_products = []
        product_ids = result.get('suggested_product_ids', [])
        if product_ids:
            try:
                products = Product.objects.filter(id__in=product_ids, is_active=True)
                # Sắp xếp đúng thứ tự ID gợi ý
                products_dict = {p.id: p for p in products}
                sorted_products = [products_dict[pid] for pid in product_ids if pid in products_dict]
                
                for p in sorted_products:
                    response_products.append({
                        'id': p.id,
                        'name': p.name,
                        'price': float(p.price),
                        'original_price': float(p.original_price) if p.original_price else None,
                        'image_url': p.image.url if p.image else '',
                        'url': f"/products/{p.slug}/"
                    })
            except Exception as e:
                print("Error fetching products:", e)
                
        return {
            'message': result.get('message', 'Xin lỗi, tôi chưa hiểu rõ ý bạn.'),
            'data': response_products,
            'suggested_replies': result.get('suggested_replies', []),
            'updated_history': updated_history
        }
        
    except Exception as e:
        print("Gemini API Error:", e)
        return {
            'message': "Xin lỗi, hiện tại hệ thống AI đang quá tải hoặc gặp sự cố. Bạn vui lòng thử lại sau nhé!",
            'data': [],
            'updated_history': chat_history
        }
