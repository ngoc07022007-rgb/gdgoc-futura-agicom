import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config import product_col

def seed_products():
    print("[*] Đang nạp Danh mục sản phẩm mẫu...")
    products = [
        {
            "id": "prod_a56",
            "text": "Điện thoại Agicom A56: Màn hình 6.5 inch, Chip Dimensity 900, RAM 8GB, Pin 5000mAh. Màu: Đen thạch anh, Xanh đại dương. Giá: 5.500.000đ."
        },
        {
            "id": "prod_a57",
            "text": "Điện thoại Agicom A57 (Premium): Màn hình AMOLED 120Hz, RAM 12GB, Bộ nhớ 256GB. Màu: Trắng ngọc trai, Đỏ Ruby. Giá: 7.200.000đ."
        },
        {
            "id": "prod_case_01",
            "text": "Ốp lưng Silicone cao cấp cho A56/A57: Chống sốc, nhiều màu sắc. Giá: 150.000đ (Sản phẩm Phụ kiện - Không đổi trả)."
        }
    ]
    
    product_col.add(
        documents=[p["text"] for p in products],
        ids=[p["id"] for p in products]
    )
    print("[SUCCESS] Đã nạp sản phẩm.")

if __name__ == "__main__":
    seed_products()