from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import models, schemas, database
from datetime import date

router = APIRouter(prefix="/sales", tags=['Sales'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SaleResponse)
def create_sale(sale_data: schemas.SaleCreate, db: Session = Depends(database.get_db)):
    # 1. Calculate total
    total = sum(item.quantity * item.price_at_sale for item in sale_data.items)
    
    # 2. Create Sale record
    new_sale = models.Sale(
        shop_name=sale_data.shop_name,
        customer_name=sale_data.customer_name,
        total_amount=total,
        payment_method=sale_data.payment_method
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    # 3. Create Sale Items
    for item in sale_data.items:
        db_item = models.SaleItem(**item.model_dump(), sale_id=new_sale.id)
        db.add(db_item)
    
    db.commit()
    return new_sale

@router.get("/summary", response_model=schemas.SalesSummary)
def get_sales_summary(db: Session = Depends(database.get_db)):
    today = date.today()
    
    total_revenue = db.query(func.sum(models.Sale.total_amount)).scalar() or 0
    total_count = db.query(models.Sale).count()
    today_count = db.query(models.Sale).filter(func.date(models.Sale.created_at) == today).count()
    avg_sale = total_revenue / total_count if total_count > 0 else 0
    
    return {
        "total_sales_count": total_count,
        "total_revenue": total_revenue,
        "today_sales_count": today_count,
        "average_sale": avg_sale
    }

@router.get("/", response_model=List[schemas.SaleResponse])
def get_all_sales(db: Session = Depends(database.get_db), search: str = None):
    query = db.query(models.Sale)
    if search:
        query = query.filter(models.Sale.customer_name.contains(search))
    return query.order_by(models.Sale.created_at.desc()).all()