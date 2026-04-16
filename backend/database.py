import os
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "agicom_system.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
Base = declarative_base()

# Lưu Log Chat để báo cáo cuối ngày
class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    customer_q = Column(Text)
    ai_a = Column(Text)
    insight = Column(String) # Ví dụ: "Khách chê đắt"
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Lưu các Task mà Agent CSKH giao cho Agent khác
class CoordinationTask(Base):
    __tablename__ = "coordination_tasks"
    id = Column(Integer, primary_key=True, index=True)
    target_agent = Column(String) # "Pricing" hoặc "Content"
    product_id = Column(String)
    instruction = Column(Text)
    status = Column(String, default="pending") # pending, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 1. Định nghĩa Model ChatMessage
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    role = Column(String)  # 'user' hoặc 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# 2. Hàm lưu tin nhắn vào DB
def save_message(db, customer_id: str, role: str, content: str):
    new_msg = ChatMessage(customer_id=customer_id, role=role, content=content)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# 3. Hàm lấy N tin nhắn gần nhất
def get_chat_history(db, customer_id: str, limit: int = 10):
    # Lấy ra tin nhắn mới nhất trước, sau đó đảo ngược lại để đúng thứ tự hội thoại
    messages = db.query(ChatMessage)\
        .filter(ChatMessage.customer_id == customer_id)\
        .order_by(desc(ChatMessage.timestamp))\
        .limit(limit)\
        .all()
    return messages[::-1] # Đảo ngược list để trả về theo thứ tự thời gian tăng dần

def init_db():
    Base.metadata.create_all(bind=engine)