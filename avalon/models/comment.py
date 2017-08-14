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


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment = Column(String(60))

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="comments")

    resource_id = Column(Integer, ForeignKey('resources.id'))
    resource = relationship("Resource", back_populates="comments")
