from pydantic import BaseModel, Field
from decimal import Decimal

class ProdutoCreate(BaseModel):
    nome: str = Field(..., example="Teclado Mecânico")
    valor_compra: Decimal = Field(..., example=180.00)
    valor_venda: Decimal = Field(..., example=299.90)
    quantidade_estoque: int = Field(..., example=10)