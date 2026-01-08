from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from decimal import Decimal

from models.schema_produtos import Produto, ProdutoUpdate
from src.core.database import get_db
from src.modules.estoque.queries import get_produtos, insert_produto, update_produto, delete_produto, check_quantidade_produto, saida_produto, entrada_produto
        
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

@router.post("/produto", status_code=status.HTTP_201_CREATED)
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

@router.put("/produto/{produto_id}")
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

@router.delete("/produto/{produto_id}", status_code=200)
async def deletar_produto(
    produto_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            check_quantidade_produto,
            {"produto_id": produto_id}
        )

        quantidade = result.scalar()

        if quantidade is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        if quantidade > 0:
            raise HTTPException(
                status_code=409,
                detail="Produto não pode ser deletado: Existe estoque disponível"
            )

        # 2️⃣ Deleta o produto
        delete_result = await db.execute(
            delete_produto,
            {"produto_id": produto_id}
        )

        deleted_id = delete_result.scalar()
        await db.commit()

        return {
            "status": "ok",
            "produto_id": deleted_id,
            "message": "Produto deletado com sucesso"
        }

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# -- Registrar saída de produto (venda)

@router.post("/produto/saida/{produto_id}", status_code=200)
async def registrar_saida_produto(
    produto_id: int,
    quantidade: float,
    db: AsyncSession = Depends(get_db)
):
    try:

        quantidade = Decimal(str(quantidade))

        # 1️⃣ Verifica a quantidade atual
        result = await db.execute(
            check_quantidade_produto,
            {"produto_id": produto_id}
        )

        quantidade_estoque = result.scalar()

        if quantidade_estoque is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        if quantidade > quantidade_estoque:
            raise HTTPException(
                status_code=409,
                detail="Quantidade insuficiente em estoque"
            )

        # 2️⃣ Calcula novo estoque
        novo_estoque = quantidade_estoque - quantidade

        # 3️⃣ Atualiza estoque + ultima_venda
        update_result = await db.execute(
            saida_produto,
            {
                "id": produto_id,
                "quantidade_estoque": novo_estoque
            }
        )

        updated = update_result.first()
        await db.commit()

        return {
            "status": "ok",
            "produto_id": updated.id,
            "nova_quantidade_estoque": updated.quantidade_estoque,
            "ultima_venda": updated.ultima_venda
        }

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
# -- Registrar entrada de produto (compra)

@router.post("/produto/entrada/{produto_id}", status_code=200)
async def registrar_entrada_produto(
    produto_id: int,
    quantidade: float,
    db: AsyncSession = Depends(get_db)
):
    try:

        quantidade = Decimal(str(quantidade))

        # 1️⃣ Verifica a quantidade atual
        result = await db.execute(
            check_quantidade_produto,
            {"produto_id": produto_id}
        )

        quantidade_estoque = result.scalar()

        if quantidade_estoque is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        # 2️⃣ Calcula novo estoque
        novo_estoque = quantidade_estoque + quantidade

        # 3️⃣ Atualiza estoque + ultima_compra
        entrada_produto_result = await db.execute(
            entrada_produto,
            {
                "id": produto_id,
                "quantidade_estoque": novo_estoque
            }
        )

        updated = entrada_produto_result.first()
        await db.commit()

        return {
            "status": "ok",
            "produto_id": updated.id,
            "nova_quantidade_estoque": updated.quantidade_estoque,
            "ultima_compra": updated.ultima_compra
        }

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )