from typing import AsyncGenerator, List
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import init_db

# WebSocket maNager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnect = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnect.append(connection)

        for conn in disconnect:
            self.disconnect(conn)

manager = ConnectionManager()

# Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando base de datos...")
    await init_db()
    print("Base de datos lista.")
    yield
    print("Apagando app...")

# Crear app
app = FastAPI(lifespan=lifespan)

# Rutas
from routes import auth, sale
app.include_router(auth.router)
app.include_router(sale.router)

# CORS 
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
