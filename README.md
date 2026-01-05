# 📦 Sistema de Controle de Estoque & Finanças

Backend desenvolvido em **FastAPI**, integrado ao **Supabase (PostgreSQL)**, com foco em organização de estoque, controle financeiro e arquitetura escalável para sistemas reais de produção.

---

## 🚀 Visão Geral

Este projeto tem como objetivo centralizar:
- 📦 **Controle de estoque**
- 💰 **Gestão financeira**
- ⚙️ **Parâmetros e configurações do sistema**

Tudo isso através de uma **API REST moderna**, segura e performática.

---

## 🧠 Decisões Técnicas

- **FastAPI**: alta performance, tipagem forte e documentação automática
- **PostgreSQL (Supabase)**: banco robusto, confiável e escalável
- **SQLAlchemy 2.0**: ORM moderno e alinhado com async
- **Alembic**: versionamento de schema e migrations
- **Pydantic v2**: validação e serialização eficiente
- **Arquitetura modular**: fácil manutenção e crescimento

---

## 🛠️ Tecnologias Utilizadas

- Python **3.11**
- FastAPI
- Uvicorn
- SQLAlchemy 2.0
- Alembic
- AsyncPG
- Pydantic & Pydantic Settings
- PostgreSQL (Supabase)
- Docker (futuro)
- Git

---

## ⚙️ Configuração do Ambiente

### 1️⃣ Requisitos
- Python **3.11.x**
- Conta no **Supabase**
- PostgreSQL habilitado

---

### 2️⃣ Criar virtual environment

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 3️⃣ Instalar dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Configurar `.env`

```env
DB_HOST=xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=senha_do_banco
DB_SSL=true
```

> As credenciais são obtidas no painel do Supabase.

---

## ▶️ Executando a Aplicação

```powershell
uvicorn src.app:app --reload
```

A API estará disponível em:
```
http://127.0.0.1:8000
```

Documentação automática:
- Swagger: `/docs`
- ReDoc: `/redoc`

---

## 🔌 Teste de Conexão com o Banco

Endpoint de healthcheck:

```json
{
  "status": "ok",
  "database": "connected",
  "result": 1
}
```

Esse retorno confirma:
- API rodando
- Conexão com Supabase ativa
- Query executada com sucesso

---

## 📦 Funcionalidades Planejadas

### Estoque
- Cadastro de produtos
- Entrada e saída
- Quantidade mínima
- Histórico de movimentações

### Financeiro
- Receitas e despesas
- Integração com estoque
- Relatórios

### Sistema
- Parâmetros globais
- Autenticação (JWT)
- Controle de permissões
- Logs e auditoria

---

## 🧪 Próximos Passos

- [ ] Inicializar Alembic
- [ ] Modelar tabelas principais
- [ ] Criar CRUD de estoque
- [ ] Implementar autenticação
- [ ] Dockerizar a aplicação

---

## 👤 Autor

**Alexandre Pereira**  
Desenvolvedor Full Stack com foco em Backend  

📫 Email: alexpln259@gmail.com  
🔗 LinkedIn: https://www.linkedin.com/in/alexandre-pereira-42213424b/

---

## 📄 Licença

Projeto em desenvolvimento para fins educacionais e profissionais.
