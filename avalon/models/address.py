from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .meta import Base


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String(60))
    phone = Column(String(60))
    note = Column(String(60))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

