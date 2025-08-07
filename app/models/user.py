import uuid
from sqlalchemy import UUID, Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.sale import Sale
from app.models.expense import Expense

class User(Base):
    __tablename__ = "users"
    
    id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name     = Column(String, nullable=False, index=True)
    username     = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    
    
    sales = relationship(Sale, back_populates="user")
    expenses = relationship(Expense, back_populates="user") 