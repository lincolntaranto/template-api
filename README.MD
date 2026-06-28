![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/lincolntaranto/template-api/ci.yml?label=CI%20/%20Tests&style=flat-square)
[![Dependabot](https://img.shields.io/badge/dependabot-active-brightgreen?style=flat-square&logo=dependabot)](https://github.com/lincolntaranto/template-api/blob/main/.github/dependabot.yml)
[![Python Version](https://img.shields.io/badge/python-3.14-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Framework: FastAPI](https://img.shields.io/badge/framework-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Linter: Ruff](https://img.shields.io/badge/linter-ruff-black?style=flat-square&logo=ruff)](https://github.com/astral-sh/ruff)
[![Deploy](https://img.shields.io/badge/deploy-render-purple)]()
[![Status](https://img.shields.io/badge/status-online-success)](https://template-api-89m8.onrender.com/docs)
[![Email: Resend](https://img.shields.io/badge/email-Resend-000000?style=flat-square&logo=resend)](https://resend.com/)

# FastAPI Template

Template base para criação de APIs REST.

---

## Tecnologias

- **FastAPI** — framework web
- **SQLAlchemy 2.0** — ORM
- **PostgreSQL** — banco de dados
- **Alembic** — migrations
- **Pydantic Settings** — configurações via `.env`
- **pwdlib (Argon2)** — hash de senha
- **PyJWT** — JWT
- **Resend + Jinja2** — envio de emails transacionais
- **Docker** — containerização

---

## Estrutura

```
template-api/
├── alembic/              # Migrations
├── core/
│   ├── config.py         # Configurações (settings)
│   ├── security.py       # JWT, hash de senha, autenticação
│   └── email/
│       ├── utils.py      # Funções de envio de email
│       └── build/        # Templates HTML dos emails
│       └── src/          # Templates MJML dos emails
├── models/
│   ├── base.py           # Engine e Base do SQLAlchemy
│   ├── session.py        # Sessão do banco
│   └── user.py           # Model de usuário
├── routes/
│   ├── auth_routes.py    # Rotas de autenticação
│   └── user_routes.py    # Rotas do usuário logado
├── schemas/
│   ├── user.py           # Schemas Pydantic
│   └── login.py          # Schemas Pydantic
├── tests/
│   ├── conftest.py       # Configurações base do pytest
│   └── test_auth.py      # Testes de autenticação
│   └── test_user.py      # Testes de C.R.U.D da rota user
├── crud.py               # Funções de acesso ao banco
├── main.py               # Entrypoint da aplicação
├── Dockerfile            # Imagem Docker da API
├── docker-compose.yml    # Orquestra API + banco
├── .env-exemplo          # Exemplo de variáveis de ambiente
└── requirements.txt
```

---

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/lincolntaranto/template-api.git
cd template-api
```

### 2. Configure o `.env`

```bash
cp .env-exemplo .env
```
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db
DATABASE_TEST_URL=postgresql://postgres:sua_senha@localhost:5432/test_db
SECRET_KEY=sua_chave_secreta
ACCESS_TOKEN_EXPIRE_MINUTES=30
EMAIL_RESET_TOKEN_EXPIRE_HOURS=48
FRONTEND_HOST=http://localhost:3000
PROJECT_NAME=Meu Projeto

# Email
RESEND_API_KEY=sua_api_key
EMAILS_FROM_EMAIL=noreply@seudominio.com
EMAILS_FROM_NAME=Meu Projeto
```

### 3. Suba os containers

```bash
docker-compose up -d
```

### 4. Rode as migrations

```bash
docker-compose exec api alembic upgrade head
```

A documentação interativa estará disponível em `http://localhost:8000/docs`.

---

## Rotas

### Auth — `/auth`

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/auth/create_user` | Cria um novo usuário | ❌ |
| POST | `/auth/login` | Login com email e senha, retorna JWT | ❌ |
| POST | `/auth/login-form` | Login via formulário OAuth2 (para o `/docs`) | ❌ |
| POST | `/auth/password-recovery/{email}` | Envia email de recuperação de senha | ❌ |
| POST | `/auth/reset-password` | Redefine a senha via token recebido por email | ❌ |

### User — `/user`

> Todas as rotas abaixo exigem autenticação via Bearer Token.

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/user/me` | Retorna dados do usuário logado |
| PATCH | `/user/password` | Atualiza a senha |
| PATCH | `/user/email` | Atualiza o email |
| PATCH | `/user/username` | Atualiza o nome |
| DELETE | `/user/delete-account` | Deleta a conta |
