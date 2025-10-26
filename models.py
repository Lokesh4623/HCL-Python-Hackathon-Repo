from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    pan_number = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=True)
    accounts = relationship("Account", back_populates="user")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(12), unique=True, nullable=False)
    account_type = Column(String(20), nullable=False)
    balance = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="accounts")
