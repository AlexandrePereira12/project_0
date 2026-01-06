from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.core.database import get_db
from src.modules.estoque.estoque import router as estoque_router

app = FastAPI(title="API Controle de Estoque e Finanças")


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
        
app.include_router(estoque_router)