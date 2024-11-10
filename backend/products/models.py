from sqlalchemy import Column, Integer, String

from backend.database import Base


class Products(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String)
    
    def __str__(self):
        return self.name

