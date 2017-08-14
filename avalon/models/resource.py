from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .meta import Base


class Resource(Base):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    title = Column(String(60))
    description = Column(String(60))
    price = Column(Float(asdecimal=True))

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="resources")

    orders = relationship("Order", back_populates="resources")
    comments = relationship("Comment", back_populates="resource")
