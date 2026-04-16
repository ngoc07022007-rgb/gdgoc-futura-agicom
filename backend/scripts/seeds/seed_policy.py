import sys
import os

# Thêm đường dẫn root vào sys.path để import được config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config import policy_col

def seed_policy():
    print("[*] Đang nạp Chính sách sàn AGICOM vào Vector DB...")
    
    # Chia nhỏ chính sách theo các đầu mục chính để AI truy xuất chính xác hơn
    policies = [
        {
            "id": "pol_gen_01",
            "content": "Nguyên tắc hoạt động AGICOM: Minh bạch thông tin, công bằng, bảo vệ người tiêu dùng, tuân thủ pháp luật Việt Nam (Nghị định 52/2013/NĐ-CP, 85/2021/NĐ-CP)."
        },
        {
            "id": "pol_return_01",
            "content": "Thời gian đổi trả: Hàng nguyên giá (30 ngày), Hàng khuyến mãi (7 ngày), Hàng tặng (7 ngày - chỉ đổi không trả). Phụ kiện không áp dụng đổi trả."
        },
        {
            "id": "pol_return_02",
            "content": "Điều kiện đổi trả: Sản phẩm chưa qua sử dụng, còn nguyên tem nhãn, có hóa đơn. Chấp nhận nếu lỗi nhà sản xuất, giao sai sản phẩm, không đúng mô tả hoặc thiếu hàng."
        },
        {
            "id": "pol_return_03",
            "content": "Chi phí đổi trả: Người bán chịu phí nếu lỗi do sản phẩm. Người mua chịu phí nếu đổi trả do nhu cầu cá nhân."
        },
        {
            "id": "pol_warranty_01",
            "content": "Chính sách bảo hành: Thời gian 6 tháng kể từ ngày mua. Áp dụng cho lỗi kỹ thuật: khóa kéo, bong keo, đứt quai, lỗi chất liệu."
        },
        {
            "id": "pol_warranty_02",
            "content": "Trường hợp không bảo hành: Hư hỏng do sử dụng sai cách, hao mòn tự nhiên, sản phẩm không còn nguyên trạng. Miễn phí phí bảo hành lỗi sản xuất."
        },
        {
            "id": "pol_outlet_01",
            "content": "Hàng Outlet: Đổi trả trong 7 ngày, không áp dụng đổi tại cửa hàng, không bảo hành. Chỉ hỗ trợ trả hàng nếu sản phẩm lỗi."
        },
        {
            "id": "pol_payment_01",
            "content": "Cơ chế thanh toán: AGICOM giữ tiền trung gian. Người mua xác nhận nhận hàng thì người bán mới nhận được tiền."
        }
    ]

    documents = [p["content"] for p in policies]
    ids = [p["id"] for p in policies]

    # Xóa cũ nạp mới (tùy chọn)
    try:
        policy_col.add(documents=documents, ids=ids)
        print(f"[SUCCESS] Đã nạp {len(ids)} mục chính sách.")
    except Exception as e:
        print(f"[ERROR] Có lỗi khi nạp: {e}")

if __name__ == "__main__":
    seed_policy()