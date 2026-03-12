import datetime
from pydantic import BaseModel,EmailStr
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config={
        "from_attributes": True
    }
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    accessToken:str
    tokenType:str

class SaleItemCreate(BaseModel):
    product_name: str
    quantity: int
    price_at_sale: float

class SaleCreate(BaseModel):
    shop_name: Optional[str] = "Main Shop"
    customer_name: Optional[str] = "Walk-in Customer"
    payment_method: str
    items: List[SaleItemCreate]

class SaleResponse(BaseModel):
    id: int
    shop_name: str
    customer_name: str
    total_amount: float
    payment_method: str
    status: str
    created_at: datetime # This now refers to the class, not the module
    
    model_config = {
        "from_attributes": True
    }

class SalesSummary(BaseModel):
    total_sales_count: int
    total_revenue: float
    today_sales_count: int
    average_sale: float