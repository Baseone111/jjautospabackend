from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,func,DateTime,Float,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable =False) 
    title = Column(String(256), nullable =False)
    content = Column(String(256), nullable=False)
    published = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                    nullable=False, 
                    server_default=func.now())
  
class User(Base):
    __tablename__ = 'users'
    email = Column(String(256),nullable=False,unique=True)
    id = Column(Integer, primary_key=True, nullable=False )
    password = Column(String(256), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                    nullable=False, 
                    server_default=func.now())
    

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String(255), default="Main Shop")
    customer_name = Column(String(255), default="Walk-in Customer")
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String(50), default="Cash") # Cash, Mobile Money, etc.
    status = Column(String(50), default="Completed")   # Completed, Voided
    created_at = Column(DateTime, server_default=func.now())

    # Relationship to items
    items = relationship("SaleItem", back_populates="sale")


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_sale = Column(Float, nullable=False)

    sale = relationship("Sale", back_populates="items")

 