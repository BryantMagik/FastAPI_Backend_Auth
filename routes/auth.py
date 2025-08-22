from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.token_service import create_access_token
from app.database import get_db
from app.models.user import User
from app.schemas import LoginData, RegisterData
from utils.hashing import hash_password, verify_password
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/login",tags=["Auth"])
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter(User.username == data.username))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        access_token = create_access_token({"sub": str(user.id)})
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error en la base de datos")

@router.post("/register", tags=["Auth"])
async def register(data: RegisterData, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(User).filter(User.username == data.username)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="Nombre de usuario ya existe.")

        new_user = User(name=data.name,username=data.username, password=hash_password(data.password))
        db.add(new_user)
        await db.commit()
        return {"message": "Usuario registrado con éxito"}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar usuario: {e}")