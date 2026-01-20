from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import get_db
from src.modules.estoque.estoque import router as estoque_router
from src.modules.caixa.caixa import router as caixa_router
from src.modules.relatorios.relatorios import router as relatorios_router

app = FastAPI(title="API Controle de Estoque e Finanças")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Substitua pelo domínio do frontend, se necessário
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

@app.get("/")
async def health_check():
    return {"status": "API rodando"}

@app.get("/health/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "result": result.scalar()
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "not connected",
            "detail": str(e)
        }

# Rotas dos módulos

app.include_router(estoque_router)
app.include_router(caixa_router)
app.include_router(relatorios_router)