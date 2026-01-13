from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from src.core.database import get_db
from src.modules.caixa.queries import check_quantidade_produto, saida_produto, entrada_produto, insert_movimentacao
        
router = APIRouter(prefix="/caixa", tags=["Caixa"])

# -- Registrar saída de produto (venda)

@router.post("/venda/{produto_id}", status_code=200)
async def registrar_saida_produto(
    produto_id: int,
    quantidade: float,
    db: AsyncSession = Depends(get_db)
):
    try:
        quantidade = Decimal(str(quantidade))

        result = await db.execute(
            check_quantidade_produto,
            {"produto_id": produto_id}
        )

        quantidade_estoque = result.scalar()

        if quantidade_estoque is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        if quantidade > quantidade_estoque:
            raise HTTPException(status_code=409, detail="Quantidade insuficiente")

        novo_estoque = quantidade_estoque - quantidade

        # Atualiza o produto
        update_result = await db.execute(
            saida_produto,
            {
                "id": produto_id,
                "quantidade_estoque": novo_estoque
            }
        )

        updated = update_result.first()

        # REGISTRA MOVIMENTAÇÃO
        await db.execute(
            insert_movimentacao,
            {
                "produto_id": produto_id,
                "tipo": "SAIDA",
                "quantidade": quantidade,
                "estoque_antes": quantidade_estoque,
                "estoque_depois": novo_estoque,
                "motivo": "Venda"
            }
        )

        await db.commit()

        return {
            "status": "ok",
            "produto_id": updated.id,
            "estoque_anterior": quantidade_estoque,
            "nova_quantidade_estoque": updated.quantidade_estoque,
            "ultima_venda": updated.ultima_venda
        }

    except:
        await db.rollback()
        raise

# -- Registrar entrada de produto (compra)

@router.post("/compra/{produto_id}", status_code=200)
async def registrar_entrada_produto(
    produto_id: int,
    quantidade: float,
    db: AsyncSession = Depends(get_db)
):
    try:
        quantidade = Decimal(str(quantidade))

        result = await db.execute(
            check_quantidade_produto,
            {"produto_id": produto_id}
        )

        quantidade_estoque = result.scalar()

        if quantidade_estoque is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        novo_estoque = quantidade_estoque + quantidade

        update_result = await db.execute(
            entrada_produto,
            {
                "id": produto_id,
                "quantidade_estoque": novo_estoque
            }
        )

        updated = update_result.first()

        # REGISTRA MOVIMENTAÇÃO
        await db.execute(
            insert_movimentacao,
            {
                "produto_id": produto_id,
                "tipo": "ENTRADA",
                "quantidade": quantidade,
                "estoque_antes": quantidade_estoque,
                "estoque_depois": novo_estoque,
                "motivo": "Compra"
            }
        )

        await db.commit()

        return {
            "status": "ok",
            "produto_id": updated.id,
            "estoque_anterior": quantidade_estoque,
            "nova_quantidade_estoque": updated.quantidade_estoque,
            "ultima_compra": updated.ultima_compra
        }

    except:
        await db.rollback()
        raise