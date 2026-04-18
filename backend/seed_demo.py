import os
import json
import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, ChatLog, CoordinationTask, ChatMessage, ReviewLog, init_db, Base, engine
from config import policy_col, product_col, resolved_qa_col, chroma_client

# 1. Cấu hình đường dẫn Mock Data (phải trùng với logic trong services.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DATA_DIR = os.path.join(BASE_DIR, "mock_data")

def create_mock_market_files():
    """Tạo các file JSON giả lập dữ liệu cào từ sàn để Agent Data Analyst đọc"""
    print("[1/5] Tạo thư mục và file mock_data...")
    if not os.path.exists(MOCK_DATA_DIR):
        os.makedirs(MOCK_DATA_DIR)

    # File cho Samsung S24 Ultra
    s24_data = {
        "sku_id": "S24-ULTRA-001",
        "internal_data": {
            "current_price": 29990000,
            "stock_level": 12,
            "cost_price": 26000000,
            "min_margin_percent": 8
        },
        "market_data": {
            "competitors": [
                {"name": "Hoàng Hà Mobile", "price": 28490000, "is_mall": True, "rating": 4.8},
                {"name": "CellphoneS", "price": 28990000, "is_mall": True, "rating": 4.9},
                {"name": "Shop Rác", "price": 25000000, "is_mall": False, "rating": 2.1}
            ],
            "customer_reviews": [
                "Máy dùng rất tốt nhưng shop giao hơi chậm",
                "Giá hơi cao so với bên Hoàng Hà",
                "Bút S-Pen rất tiện lợi cho công việc"
            ]
        }
    }

    # File cho Cáp Anker 100W (Kịch bản rủi ro)
    anker_data = {
        "sku_id": "ANKER-100W-01",
        "internal_data": {
            "current_price": 350000,
            "stock_level": 150,
            "cost_price": 180000,
            "min_margin_percent": 15
        },
        "market_data": {
            "competitors": [
                {"name": "Anker Official", "price": 340000, "is_mall": True, "rating": 4.9}
            ],
            "customer_reviews": [
                "Sạc nhanh, dây bền",
                "Dây hơi nóng khi sạc Macbook",
                "Mới dùng 1 tuần đã hỏng đầu cắm"
            ]
        }
    }

    with open(os.path.join(MOCK_DATA_DIR, "S24-ULTRA-001-raw.json"), "w", encoding="utf-8") as f:
        json.dump(s24_data, f, ensure_ascii=False, indent=4)
    with open(os.path.join(MOCK_DATA_DIR, "ANKER-100W-01-raw.json"), "w", encoding="utf-8") as f:
        json.dump(anker_data, f, ensure_ascii=False, indent=4)

def seed_sql_data(db: Session):
    print("[2/5] Đang dọn dẹp và nạp dữ liệu SQL (SQLite)...")
    # Xóa sạch dữ liệu cũ
    db.query(ChatMessage).delete()
    db.query(ChatLog).delete()
    db.query(CoordinationTask).delete()
    db.query(ReviewLog).delete()
    db.commit()

    now = datetime.datetime.utcnow()

    # --- Nạp ReviewLog (Tạo khủng hoảng cho cáp Anker) ---
    reviews = [
        ReviewLog(product_id="ANKER-100W-01", rating=1, review_text="Sạc được 3 ngày thì hỏng, dây nóng ran. Quá thất vọng!", customer_name="Hoàng Mạnh", ai_insight="Cảnh báo: Lỗi chip quản lý dòng điện (Lô T03)", timestamp=now - datetime.timedelta(hours=10)),
        ReviewLog(product_id="ANKER-100W-01", rating=2, review_text="Giao hàng nhanh nhưng cáp dùng chập chờn lúc được lúc không.", customer_name="Lê Văn C", ai_insight="Vấn đề tiếp xúc đầu cắm USB-C", timestamp=now - datetime.timedelta(hours=5)),
        ReviewLog(product_id="S24-ULTRA-001", rating=5, review_text="Máy quá đẹp, nguyên seal, shop tư vấn 1h sáng vẫn rep. Ưng!", customer_name="Nguyễn Tuấn", ai_insight="Khen ngợi tốc độ phản hồi CSKH", timestamp=now - datetime.timedelta(days=1)),
    ]
    db.add_all(reviews)

    # --- Nạp ChatLog (Dữ liệu cho Sensor Insight & Daily Summary) ---
    chat_logs = [
        ChatLog(customer_q="Bên Hoàng Hà bán S24 Ultra rẻ hơn shop 500k, shop có giảm không?", ai_a="Dạ bên em cam kết hàng chính hãng và có tặng kèm ốp Spigen 350k ạ.", insight="Khách so sánh giá với đối thủ Hoàng Hà", timestamp=now - datetime.timedelta(hours=2)),
        ChatLog(customer_q="Cáp sạc Anker mới mua 1 tuần đã hỏng, shop làm ăn gì kỳ vậy?", ai_a="Dạ em rất tiếc, em đã chuyển thông tin cho quản lý bảo hành xử lý ngay ạ.", insight="Khiếu nại chất lượng sản phẩm (Anker 100W)", timestamp=now - datetime.timedelta(hours=1)),
        ChatLog(customer_q="Shop có trả góp qua thẻ tín dụng Sacombank không?", ai_a="Dạ shop có hỗ trợ trả góp 0% qua thẻ Sacombank kỳ hạn đến 12 tháng ạ.", insight="Khách quan tâm phương thức thanh toán trả góp", timestamp=now - datetime.timedelta(minutes=30)),
    ]
    db.add_all(chat_logs)

    # --- Nạp CoordinationTask (Các nhiệm vụ AI giao cho người) ---
    tasks = [
        CoordinationTask(target_agent="RiskManager", product_id="ANKER-100W-01", instruction="KHẨN CẤP: Có 2 review 1-2 sao và khách phàn nàn về cáp Anker bị cháy nóng. Kiểm tra ngay lô hàng nhập ngày 01/10.", status="pending"),
        CoordinationTask(target_agent="Pricing", product_id="S24-ULTRA-001", instruction="Đối thủ Hoàng Hà đang giảm giá mạnh. Đề xuất tạo voucher 500k cho khách cũ để giữ chân.", status="pending"),
        CoordinationTask(target_agent="Content", product_id="S24-ULTRA-001", instruction="Nhiều khách hỏi về thời lượng pin thực tế. Cần bổ sung video test pin vào mô tả sản phẩm.", status="pending")
    ]
    db.add_all(tasks)

    # --- Nạp ChatMessage (Lịch sử hội thoại thực để demo chat-v3) ---
    vip_id = "customer_vip_88"
    msgs = [
        ChatMessage(customer_id=vip_id, role="user", content="Chào shop, mình là khách quen đây."),
        ChatMessage(customer_id=vip_id, role="assistant", content="Dạ chào anh/chị, rất vui được gặp lại anh/chị! Shop có thể hỗ trợ gì cho mình ạ?"),
        ChatMessage(customer_id=vip_id, role="user", content="Mình định lấy thêm 3 cái cáp Anker 100W cho công ty, có bớt không shop?"),
        ChatMessage(customer_id=vip_id, role="assistant", content="Dạ với khách VIP, em giảm thêm 10% tổng đơn phụ kiện và tặng kèm túi đựng cáp ạ. Mình có muốn chốt đơn luôn không ạ?")
    ]
    db.add_all(msgs)

    db.commit()

def seed_vector_data():
    print("[3/5] Đang nạp kiến thức vào Vector DB (ChromaDB)...")
    
    # 1. Chính sách
    policies = [
        "Chính sách bảo hành: Điện thoại bảo hành 12 tháng chính hãng. Phụ kiện bảo hành 6 tháng 1 đổi 1.",
        "Chính sách vận chuyển: Freeship đơn từ 500k. Giao hỏa tốc nội thành trong 2h.",
        "Chính sách đổi trả: Lỗi nhà sản xuất đổi mới trong 7 ngày đầu. Yêu cầu còn nguyên hộp."
    ]
    policy_col.add(documents=policies, ids=[f"pol_{i}" for i in range(len(policies))])

    # 2. Sản phẩm (Chi tiết để AI tư vấn)
    products = [
        "Samsung S24 Ultra: Chip Snapdragon 8 Gen 3, Camera 200MP, Pin 5000mAh, Sạc nhanh 45W, Có bút S-Pen.",
        "Cáp Anker 100W: Dài 1.8m, bọc dù, hỗ trợ PD sạc cho cả Macbook và Laptop.",
        "Tai nghe AirPods Pro 2: Chống ồn chủ động ANC, Chip H2, Cổng sạc USB-C."
    ]
    product_col.add(documents=products, ids=[f"prod_{i}" for i in range(len(products))])

    # 3. Kinh nghiệm đã học
    qas = [
        "Q: Shop có trả góp không? A: Dạ shop trả góp 0% qua thẻ tín dụng và các công ty tài chính như HD Saison.",
        "Q: Hàng chính hãng hay xách tay? A: Agicom cam kết 100% hàng chính hãng VN/A, nguyên seal chưa kích hoạt."
    ]
    resolved_qa_col.add(documents=qas, ids=[f"qa_{i}" for i in range(len(qas))])

def main():
    print("=== AGICOM SYSTEM SEEDER V2.0 ===")
    init_db()
    db = SessionLocal()
    
    try:
        create_mock_market_files()
        seed_sql_data(db)
        seed_vector_data()
        
        print("\n[SUCCESS] Seed dữ liệu hoàn tất!")
        print(f"- SQL: {db.query(ReviewLog).count()} Reviews, {db.query(CoordinationTask).count()} Tasks.")
        print(f"- Mock Files: Đã tạo tại {MOCK_DATA_DIR}")
        print("- Vector DB: Đã nạp 8 tài liệu kiến thức.")
        print("\nLưu ý: Nếu Backend dùng EphemeralClient, bạn cần nạp lại Vector DB mỗi khi khởi động lại server.")
        
    except Exception as e:
        print(f"\n[ERROR] Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()