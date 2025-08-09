from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sale import Sale
from app.models.user import User
from app.auth.token_service import get_current_user
from app.database import get_db
from app.schemas import SalesData

router = APIRouter()

@router.post("/sales",tags=["Sale"])
async def create_sale(data: SalesData, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        new_sale = Sale(**data.dict(), user_id= current_user.id)
        
        db.add(new_sale)
        await db.commit()
        await db.refresh(new_sale)
        
        return new_sale
    except Exception as e:
        await db.rollback()
        
        raise HTTPException(status_code=500, detail=str(e))

        
        
        
    
