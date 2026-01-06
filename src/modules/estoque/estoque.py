from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.schema_produtos import Produto, ProdutoUpdate
from src.core.database import get_db
from src.modules.estoque.queries import get_produtos, insert_produto, update_produto
        
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
    produto: Produto,
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

@router.put("/produtos/{produto_id}")
async def editar_produto(
    produto_id: int,
    produto: ProdutoUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = produto.model_dump(exclude_unset=True)

        if not payload:
            raise HTTPException(
                status_code=400,
                detail="Nenhum campo enviado para atualização"
            )

        payload["id"] = produto_id

        result = await db.execute(update_produto, payload)
        updated_id = result.scalar()

        if not updated_id:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        await db.commit()

        return {
            "status": "ok",
            "produto_id": updated_id
        }

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )