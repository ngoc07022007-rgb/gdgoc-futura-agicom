import os
import json
from fastapi import HTTPException
from google.genai import types
from config import policy_col, product_col, resolved_qa_col, client
from prompts import DATA_ANALYST_PROMPT, CHAT_RAG_PROMPT, LEARNING_EXTRACTOR_PROMPT, STRATEGY_SYSTEM_PROMPT
from models import MarketInsight
from database import SessionLocal, CoordinationTask, ChatLog

def fetch_raw_market_data(sku_id: str) -> dict:
    file_path = f"backend/mock_data/{sku_id}-raw.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Không tìm thấy file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

async def analyze_raw_data_phase1(sku_id: str) -> MarketInsight:
    print(f"[*] PHASE 1: Đang trích xuất dữ liệu thô cho {sku_id}...")
    
    # 1. Đọc dữ liệu thô
    raw_data = fetch_raw_market_data(sku_id)
    user_prompt = f"Dữ liệu thô từ sàn: {json.dumps(raw_data, ensure_ascii=False)}"
    
    # 2. Gọi Gemini đóng vai Data Analyst
    response = await client.aio.models.generate_content(
        model="gemini-flash-latest",
        contents=[DATA_ANALYST_PROMPT, user_prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MarketInsight,
            http_options={'timeout': 45000}
        )
    )
    
    if not response.text:
        raise HTTPException(status_code=500, detail="Lỗi Phase 1: Không có phản hồi.")
        
    clean_text = response.text.replace("```json", "").replace("```", "").strip()
    insight_dict = json.loads(clean_text)
    
    print(f"[*] PHASE 1 HOÀN TẤT: {insight_dict['analyst_summary']}")
    
    # Trả về cả Insight đã lọc và Internal Data gốc (để lát nữa đưa cho Strategist)
    return {
        "insight": insight_dict,
        "internal_data": raw_data["internal_data"]
    }

async def analyze_strategy_slow_track(data: dict):
    """THINK -> PLAN: Luồng chậm (Phân tích giá & Nội dung)"""
    prompt = f"Phân tích dữ liệu thị trường sau và đưa ra chiến lược định giá/nội dung: {data}"
    
    response = await client.aio.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    # Trong thực tế, sẽ có response_schema ở đây
    return {"track": "Slow Track", "strategy": "Pricing & Content Proposal", "details": response.text}

async def customer_care_fast_track(data: dict):
    """THINK -> PLAN -> GUARDRAIL: Luồng nhanh (CSKH)"""
    chat_history = data.get("message", "")
    
    # Prompt tích hợp Safety Guardrail
    prompt = f"""Bạn là Agent CSKH. Trả lời tin nhắn sau: '{chat_history}'.
    Đồng thời tự đánh giá độ tự tin (confidence) của bạn từ 0.0 đến 1.0. 
    Nếu bạn không chắc chắn hoặc khách hàng đang giận dữ, hãy cho confidence < 0.7.
    Trả về định dạng JSON: {{"reply": "...", "confidence": 0.9}}"""
    
    response = await client.aio.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    
    try:
        result = json.loads(response.text)
        confidence = result.get("confidence", 1.0)
        
        # ACT: SAFETY GUARDRAIL LOGIC
        if confidence >= 0.7:
            return {"track": "Fast Track", "action": "Auto Reply to Customers", "message": result["reply"], "status": "Safe"}
        else:
            return {"track": "Fast Track", "action": "Send Proposals to Dashboard", "draft": result["reply"], "status": "Flagged / Low Confidence"}
    except:
        return {"track": "Fast Track", "status": "Error parsing JSON"}

# Cập nhật hàm cskh_rag_service trong services.py

async def cskh_rag_service(customer_text: str, brand_tone: str):
    # 1. Retrieval (Tìm kiếm context) - Giữ nguyên logic cũ của bạn
    policy_hits = policy_col.query(query_texts=[customer_text], n_results=2)
    product_hits = product_col.query(query_texts=[customer_text], n_results=2)
    qa_hits = resolved_qa_col.query(query_texts=[customer_text], n_results=2)
    
    def get_all_hits(hits):
        if hits and hits.get('documents') and len(hits['documents'][0]) > 0:
            return "\n- ".join(hits['documents'][0])
        return "Không có thông tin cụ thể."

    context = f"""
    CÁC THÔNG TIN TÌM THẤY:
    Quy định: {get_all_hits(policy_hits)}
    Sản phẩm: {get_all_hits(product_hits)}
    Kinh nghiệm: {get_all_hits(qa_hits)}
    """

    # 2. Generation (Gọi AI phân tích cảm xúc và trả lời)
    user_prompt = CHAT_RAG_PROMPT.format(context=context, brand_tone=brand_tone)
    
    response = await client.aio.models.generate_content(
        model="gemini-flash-latest",
        contents=[user_prompt, f"Tin nhắn khách: {customer_text}"],
        config={"response_mime_type": "application/json"}
    )
    
    result = json.loads(response.text)

    # 3. Logic Guardrail dựa trên Sentiment
    sentiment = result.get("sentiment_analysis", "bình thường")
    
    # NÂNG CẤP: Nếu khách đang tức giận, không bao giờ cho phép Auto-Reply
    if sentiment == "tức giận":
        result["is_safe"] = False
        print(f"[!] CẢNH BÁO: Phát hiện khách hàng đang tức giận!")

    # 4. Coordination (Điều phối nếu có insight)
    if result.get("sensor_insight"):
        # Trích xuất Product ID từ ngữ cảnh (giả định đang chat về A56)
        await coordinate_agents(result["sensor_insight"], "A56")

    return result

async def learn_from_human_service(customer_q: str, human_a: str):
    """Lưu cặp Q&A đã được con người duyệt vào Vector DB"""
    try:
        # 1. Chuẩn bị Prompt
        prompt = LEARNING_EXTRACTOR_PROMPT.format(chat_log=f"Q: {customer_q}, A: {human_a}")
        
        # 2. Gọi Gemini (Thêm config response_mime_type để ép AI trả về JSON)
        response = await client.aio.models.generate_content(
            model="gemini-flash-latest", 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        if not response.text:
            raise HTTPException(status_code=500, detail="AI không trả về kết quả để học.")

        # 3. LÀM SẠCH TEXT (Quan trọng: Xử lý lỗi JSONDecodeError)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # 4. Parse JSON và lưu vào DB
        data = json.loads(clean_text)
        
        # Tạo ID duy nhất bằng cách băm nội dung câu hỏi
        import hashlib
        doc_id = hashlib.md5(data['question'].encode()).hexdigest()

        resolved_qa_col.add(
            documents=[f"Q: {data['question']} A: {data['answer']}"],
            ids=[f"qa_{doc_id}"]
        )
        
        print(f"[*] Đã học thành công kiến thức mới: {data['question']}")
        return {"status": "Learned successfully", "data_saved": data}

    except json.JSONDecodeError as e:
        print(f"LỖI PARSE JSON: {response.text}")
        raise HTTPException(status_code=500, detail="AI trả về format JSON không hợp lệ.")
    except Exception as e:
        print(f"LỖI HỌC TẬP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def coordinate_agents(insight_text: str, product_id: str):
    """
    Dựa vào insight từ CSKH để tạo 'Task' cho các Agent khác.
    """
    insight_text = insight_text.lower()
    
    # 1. Nếu insight liên quan đến GIÁ
    if any(word in insight_text for word in ["giá", "đắt", "rẻ", "chi phí", "giảm giá"]):
        print(f"[Trigger] -> Gửi yêu cầu cho PRICING AGENT: Kiểm tra lại giá mã {product_id}")
        # Logic: Gọi hàm analyze_strategy_slow_track() hoặc đánh dấu flag cho bộ phận giá
        
    # 2. Nếu insight liên quan đến THÔNG TIN/MÀU SẮC (Thiếu hàng)
    if any(word in insight_text for word in ["màu", "không có", "hỏi thêm", "thông tin"]):
        print(f"[Trigger] -> Gửi yêu cầu cho CONTENT AGENT: Cập nhật mô tả sản phẩm {product_id}")
        # Logic: Tạo một yêu cầu sửa bài đăng trên sàn

async def full_strategy_pipeline(sku_id: str, shop_profile: dict):
    """KẾT NỐI PHASE 1 & PHASE 2"""
    
    # 1. Chạy Phase 1: Data Analyst
    # Giả sử hàm analyze_raw_data_phase1 đã có sẵn từ code cũ của bạn
    phase1_result = await analyze_raw_data_phase1(sku_id)
    insight = phase1_result["insight"]
    internal = phase1_result["internal_data"]

    # 2. Chạy Phase 2: Strategist (Sử dụng STRATEGY_SYSTEM_PROMPT)
    # Gom tất cả dữ liệu lại để AI ra quyết định
    combined_data = {
        "market_insight": insight,
        "internal_data": internal,
        "shop_profile": shop_profile
    }

    user_prompt = f"Dữ liệu tổng hợp: {json.dumps(combined_data, ensure_ascii=False)}"
    
    response = await client.aio.models.generate_content(
        model="gemini-flash-latest",
        contents=[STRATEGY_SYSTEM_PROMPT, user_prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            # Giả sử bạn dùng StrategyProposal model đã định nghĩa ở models.py
        )
    )
    
    return json.loads(response.text)

async def coordinate_agents(insight_text: str, product_id: str):
    """BIẾN INSIGHT THÀNH HÀNH ĐỘNG THỰC TẾ"""
    db = SessionLocal()
    target = None
    instruction = ""

    # Logic phân loại đơn giản
    if any(word in insight_text.lower() for word in ["giá", "đắt", "rẻ"]):
        target = "Pricing"
        instruction = f"Khách hàng phản hồi về giá: {insight_text}. Kiểm tra lại biên lợi nhuận và giá đối thủ."
    
    if any(word in insight_text.lower() for word in ["màu", "thông tin", "ảnh"]):
        target = "Content"
        instruction = f"Khách hàng thắc mắc về nội dung: {insight_text}. Cập nhật lại mô tả sản phẩm."

    if target:
        new_task = CoordinationTask(
            target_agent=target,
            product_id=product_id,
            instruction=instruction
        )
        db.add(new_task)
        db.commit()
        print(f"[*] Đã tạo Task cho {target} Agent!")
    db.close()