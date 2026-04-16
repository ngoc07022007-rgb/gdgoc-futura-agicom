import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database import SessionLocal, ChatMessage, init_db

def seed_chat_history():
    print("[*] Đang tạo lịch sử hội thoại giả lập cho khách 'customer_001'...")
    init_db()
    db = SessionLocal()

    # Kịch bản: Khách đã hỏi về A56 và đang phân vân về giá
    history = [
        ChatMessage(customer_id="customer_001", role="user", content="Chào shop, mình muốn hỏi về con A56"),
        ChatMessage(customer_id="customer_001", role="assistant", content="Dạ chào bạn, Agicom A56 hiện có sẵn màu Đen và Xanh ạ. Bạn cần tư vấn kỹ thuật hay ưu đãi ạ?"),
        ChatMessage(customer_id="customer_001", role="user", content="Máy này có được freeship không bạn?"),
        ChatMessage(customer_id="customer_001", role="assistant", content="Dạ có, với đơn hàng trên 500k như A56 thì bên mình miễn phí vận chuyển toàn quốc ạ.")
    ]

    db.add_all(history)
    db.commit()
    db.close()
    print("[SUCCESS] Đã tạo lịch sử chat. Bây giờ nếu bạn chat với ID 'customer_001', AI sẽ nhớ các câu trên.")

if __name__ == "__main__":
    seed_chat_history()