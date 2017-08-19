import enum
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Enum,
)
from sqlalchemy.orm import relationship
from .meta import Base


class UserRole(enum.IntEnum):
    admin = 1
    manager = 2
    unconfirmed = 3


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(60), unique=True)
    email = Column(String(60), unique=True)
    fullname = Column(String(60), nullable=False)
    role = Column(Enum(UserRole, name='UserRole'))
    addresses = relationship("Address", back_populates="user")
    resources = relationship("Resource", back_populates="owner")
    comments = relationship("Comment", back_populates="author")
    sold = relationship("Order", back_populates="seller", foreign_keys="[Order.seller_id]")
    bought = relationship("Order", back_populates="buyer", foreign_keys="[Order.buyer_id]")
