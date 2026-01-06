from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.schema_produtos import ProdutoCreate
from src.core.database import get_db
from src.modules.estoque.queries import get_produtos,insert_produto
        
router = APIRouter(prefix="/estoque", tags=["Estoque"])

@router.get("/", status_code=200)
async def listar_produtos(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(get_produtos)

    produtos = result.mappings().all()

    return {
        "data": produtos
    }

@router.post("/produtos", status_code=status.HTTP_201_CREATED)
async def criar_produto(
    produto: ProdutoCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            insert_produto,
            {
                "nome": produto.nome,
                "valor_compra": produto.valor_compra,
                "valor_venda": produto.valor_venda,
                "quantidade_estoque": produto.quantidade_estoque,
            }
        )

        produto_id = result.scalar()
        await db.commit()

        return {
            "status": "ok",
            "produto_id": produto_id
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
