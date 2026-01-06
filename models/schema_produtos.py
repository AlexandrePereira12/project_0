from pydantic import BaseModel, Field
from decimal import Decimal

class Produto(BaseModel):
    nome: str = Field(..., example="Teclado Mecânico")
    valor_compra: Decimal = Field(..., example=180.00)
    valor_venda: Decimal = Field(..., example=299.90)
    quantidade_estoque: int = Field(..., example=10)
    
class ProdutoUpdate(BaseModel):
    nome: str | None = None
    valor_compra: float | None = None
    valor_venda: float | None = None
    quantidade_estoque: int | None = None
    