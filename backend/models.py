from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Flashcard(Base):
    __tablename__ = "flashcards"  # Đổi tên bảng

    id = Column(Integer, primary_key=True, index=True)
    front = Column(String(255), nullable=False)  # Đổi từ title
    back = Column(Text, nullable=False)         # Đổi từ content
    created_at = Column(DateTime(timezone=True), server_default=func.now())

