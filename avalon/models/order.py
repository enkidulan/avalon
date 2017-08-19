import enum
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship

from .meta import Base


class OrderStatus(enum.IntEnum):
    admin = 1
    manager = 2
    unconfirmed = 3


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    status = Column(Enum(OrderStatus, name='OrderStatus'))

    price = Column(Float(asdecimal=True))
    feedback = Column(Text)

    delivery_address_id = Column(Integer, ForeignKey('addresses.id'))
    delivery_address = relationship("Address")

    resources_id = Column(Integer, ForeignKey('resources.id'))
    resources = relationship("Resource", back_populates="orders")

    seller_id = Column(Integer, ForeignKey('users.id'))
    seller = relationship(
        "User", back_populates="sold", foreign_keys=[seller_id])

    buyer_id = Column(Integer, ForeignKey('users.id'))
    buyer = relationship(
        "User", back_populates="bought", foreign_keys=[buyer_id])
