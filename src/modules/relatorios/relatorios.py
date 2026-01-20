from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, time, datetime
from fastapi import Query
from typing import Optional

from src.modules.relatorios.queries import relatorio_vendas_periodo
from src.core.database import get_db

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/vendas", status_code=200)
async def relatorio_vendas(
    data_inicio: date = Query(..., description="Data de início do período (AAAA-MM-DD)"),
    data_fim: date = Query(..., description="Data de fim do período (AAAA-MM-DD)"),
    produto_id: Optional[int] = Query(None, description="ID do produto para filtrar o relatório (opcional)"),
    db: AsyncSession = Depends(get_db)
):
    try:
        if (data_fim - data_inicio).days > 31:
            raise HTTPException(
                status_code=400,
                detail="O período máximo permitido é de 31 dias"
            )

        inicio_dt = datetime.combine(data_inicio, time.min)
        fim_dt = datetime.combine(data_fim, time.max)

        result = await db.execute(
            relatorio_vendas_periodo,
            {
                "data_inicio": inicio_dt,
                "data_fim": fim_dt,
                "produto_id": produto_id
            }
        )

        rows = result.mappings().all()

        return {
            "periodo": {
                "inicio": data_inicio,
                "fim": data_fim
            },
            "total_produtos": len(rows),
            "vendas": rows
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
