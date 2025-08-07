import uuid
from sqlalchemy import Column, Date, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    cubos = Column(Integer, default=0)
    escamas = Column(Integer, default=0)
    pilet = Column(Integer, default=0)
    euros = Column(Float, default=0.0)

    user = relationship("User", back_populates="sales")