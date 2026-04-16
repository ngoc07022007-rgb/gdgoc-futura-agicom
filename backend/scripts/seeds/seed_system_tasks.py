import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database import SessionLocal, ChatLog, CoordinationTask, init_db

def seed_system_tasks():
    print("[*] Đang nạp dữ liệu điều phối hệ thống...")
    init_db()
    db = SessionLocal()

    # 1. Tạo Log chứa Insight (Để báo cáo Sentiment)
    logs = [
        ChatLog(
            customer_q="Sản phẩm lỗi rồi shop ơi, tôi muốn trả hàng gấp!",
            ai_a="Dạ em rất tiếc, em đã gửi yêu cầu đổi trả cho bộ phận kho ạ.",
            insight="Khách hàng bức xúc vì lỗi sản phẩm (A56)",
            timestamp=datetime.datetime.now()
        ),
        ChatLog(
            customer_q="Giá bên này cao hơn Shopee Mall 200k lận.",
            ai_a="Dạ bên em cam kết hàng chính hãng bảo hành 6 tháng ạ.",
            insight="Khách chê giá cao so với thị trường",
            timestamp=datetime.datetime.now()
        )
    ]

    # 2. Tạo Task cho các Agent khác (Để báo cáo Growth/Risk)
    tasks = [
        CoordinationTask(
            target_agent="RiskManager",
            product_id="A56",
            instruction="CẢNH BÁO: Tỷ lệ khách hỏi về lỗi màn hình tăng 15% trong hôm nay.",
            status="pending"
        ),
        CoordinationTask(
            target_agent="Pricing",
            product_id="A56",
            instruction="Đề xuất: Tạo voucher giảm 200k để cạnh tranh với Shopee Mall.",
            status="pending"
        ),
        CoordinationTask(
            target_agent="Content",
            product_id="A57",
            instruction="Cập nhật thêm video quay cận cảnh màu Đỏ Ruby vì khách hỏi nhiều.",
            status="pending"
        )
    ]

    db.add_all(logs)
    db.add_all(tasks)
    db.commit()
    db.close()
    print("[SUCCESS] Đã nạp dữ liệu Daily Summary.")

if __name__ == "__main__":
    seed_system_tasks()