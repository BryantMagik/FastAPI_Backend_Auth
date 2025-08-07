import uuid
from sqlalchemy import Column, Date, Float, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tipo = Column(String, nullable=False)
    euros = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)

    user = relationship("User", back_populates="expenses")
