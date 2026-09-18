

from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy import Column

from database import Base



class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    published_date = Column(Date, nullable=True)









