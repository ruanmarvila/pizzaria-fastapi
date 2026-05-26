# Pizzaria API:

Uma API RESTful assíncrona para gerenciamento de uma pizzaria, construída com Python e FastAPI. O projeto conta com controle de permissões (Usuário vs Admin), autenticação JWT e persistência de dados com deleção lógica (*soft delete*).

## Funcionalidades:

### Clientes:
- **Cadastro & Login:** Criação de conta e autenticação via tokens JWT.
- **Gerenciamento de Conta:** Opção de desativar a própria conta (*soft delete*).
- **Pedidos:** Criar pedidos, adicionar itens (pizzas) e cancelar pedidos pendentes.
- **Histórico:** Listagem de todos os pedidos realizados pelo usuário.

### Administradores:
- **Gestão do Sistema:** Permissão para exclusão definitiva (*hard delete*) de usuários e gerenciamento global do sistema.

## Tecnologias Utilizadas:

- **Python 3.11+**
- **FastAPI:** Framework web moderno e de alto desempenho.
- **SQLite + Aiosqlite:** Banco de dados local com suporte a operações assíncronas.
- **SQLAlchemy & Alembic:** ORM para comunicação com o banco e controle de migrações.
- **PyJWT & Argon2:** Criptografia de senhas e geração de tokens de acesso.

## Como Rodar o Projeto Localmente

### Pré-requisitos:
- Python instalado na máquina.

### Passo a Passo:

1. **Clone o repositório:**
   
```bash
   git clone https://github.com/ruanmarvila/pizzaria-fastapi/
   cd pizzaria-fastapi
```

2. **Crie um ambiente virtual:**

```bash
   python -m venv .venv

   # Windows:
   .venv\Scripts\activate

   # Linux ou Mac:
   source .venv/bin/activate
```

3. **Instale as dependências:**

```bash
   pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

    Crie um .env na raiz
```properties
   SECRET_KEY=sua_chave_secreta_aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
 ```

6. **Rode as migrações:**
```bash
   alembic upgrade head
```

6. **Inicie o servidor:**
```bash
   uvicorn app.main:app --reload
```

## Documentação da API:

O FastAPI cria automaticamente uma documentação interativa. Com o servidor rodando, você pode acessar e testar os endpoints através dos links:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc
