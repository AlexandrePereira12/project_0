from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from src.core.database import get_db
from src.modules.caixa.queries import check_quantidade_produto, saida_produto, entrada_produto, insert_movimentacao, get_movimentacoes
        
router = APIRouter(prefix="/caixa", tags=["Caixa"])

@router.get("/", status_code=200)
async def listar_movimentacoes(
    motivo: str = Query(..., regex="^(Venda|Compra)$"),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        get_movimentacoes,
        {
            "motivo": motivo,
            "limit": limit,
        }
    )

    movimentacoes = result.mappings().all()

    return {
        "data": movimentacoes
    }

# -- Registrar saída de produto (venda)

@router.post("/venda", status_code=200)
async def registrar_saida_produtos(
    produtos: list[dict],  # Exemplo: [{"produto_id": 1, "quantidade": 2, "forma_pagamento": "DINHEIRO"}]
    db: AsyncSession = Depends(get_db)
):
    resultados = []

    try:
        for item in produtos:
            produto_id = item.get("produto_id")
            quantidade = item.get("quantidade")
            forma_pagamento = item.get("forma_pagamento")

            if not produto_id or not quantidade or not forma_pagamento:
                raise HTTPException(status_code=400, detail="Dados incompletos para um dos produtos")

            if quantidade <= 0:
                raise HTTPException(status_code=400, detail=f"A quantidade para o produto {produto_id} deve ser maior que zero")

            quantidade = Decimal(str(quantidade))

            result = await db.execute(
                check_quantidade_produto,
                {"produto_id": produto_id}
            )

            quantidade_estoque = result.scalar()

            if quantidade_estoque is None:
                raise HTTPException(status_code=404, detail=f"Produto com ID {produto_id} não encontrado")

            if quantidade > quantidade_estoque:
                raise HTTPException(status_code=409, detail=f"Quantidade insuficiente para o produto {produto_id}")

            novo_estoque = quantidade_estoque - quantidade

            await db.execute(
                saida_produto,
                {
                    "id": produto_id,
                    "quantidade_estoque": novo_estoque
                }
            )

            await db.execute(
                insert_movimentacao,
                {
                    "produto_id": produto_id,
                    "tipo": "SAIDA",
                    "quantidade": quantidade,
                    "estoque_antes": quantidade_estoque,
                    "estoque_depois": novo_estoque,
                    "motivo": "VENDA",
                    "forma_pagamento": forma_pagamento
                }
            )

            resultados.append({
                "produto_id": produto_id,
                "quantidade": float(quantidade),
                "forma_pagamento": forma_pagamento,
                "estoque_anterior": float(quantidade_estoque),
                "novo_estoque": float(novo_estoque)
            })

        await db.commit()

        return {
            "status": "ok",
            "resultados": resultados
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao registrar saída: {str(e)}")

# -- Registrar entrada de produto (compra)

@router.post("/compra/{produto_id}", status_code=200)
async def registrar_entrada_produto(
    produto_id: int,
    quantidade: float,
    forma_pagamento: str,
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

        await db.execute(
            insert_movimentacao,
            {
                "produto_id": produto_id,
                "tipo": "ENTRADA",
                "quantidade": quantidade,
                "estoque_antes": quantidade_estoque,
                "estoque_depois": novo_estoque,
                "motivo": "COMPRA",
                "forma_pagamento": forma_pagamento
            }
        )

        await db.commit()

        return {
            "status": "ok",
            "produto_id": produto_id,
            "quantidade": float(quantidade),
            "forma_pagamento": forma_pagamento,
            "estoque_anterior": float(quantidade_estoque),
            "nova_quantidade_estoque": float(novo_estoque),
            "ultima_compra": updated.ultima_compra
        }

    except Exception:
        await db.rollback()
        raise