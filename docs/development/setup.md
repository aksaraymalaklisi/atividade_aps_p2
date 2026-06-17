# Configuração do Ambiente de Desenvolvimento

## Pré-requisitos

- **Docker Desktop** (Windows/macOS) ou **Docker Engine** (Linux)
- **Git**
- (Opcional) **Python 3.14+** — para rodar backend fora do Docker
- (Opcional) **Node.js 24+** — para rodar frontend fora do Docker

## Quick Start (Docker)

A forma mais rápida de rodar tudo:

```bash
# Clone o repositório
git clone https://github.com/<user>/atividade_aps_p2.git
cd atividade_aps_p2

# Suba todos os serviços (DB + backend + frontend)
docker compose -f compose.dev.yml up --build
```

Acesse:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/docs/ (Swagger)
- **PostgreSQL:** localhost:5432 (user: `postgres`, password: `postgres`)

## Desenvolvimento Local (sem Docker)

### Backend

```bash
cd backend

# Criar venv e instalar dependências
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate          # Windows

pip install -r requirements/development.txt

# Subir apenas o banco via Docker
docker compose -f ../compose.dev.yml up db -d

# Rodar migrations
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Rodar servidor de desenvolvimento
python manage.py runserver
```

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Rodar servidor de desenvolvimento
npm run dev
```

## Comandos Úteis

### Backend

| Comando | Descrição |
|---|---|
| `python manage.py migrate` | Aplicar migrations |
| `python manage.py makemigrations` | Criar novas migrations |
| `python manage.py createsuperuser` | Criar usuário admin |
| `pytest` | Rodar testes |
| `pytest --cov=apps` | Testes com cobertura |
| `ruff check .` | Verificar lint |
| `ruff format .` | Formatar código |
| `mypy apps/ core/` | Type check |

### Frontend

| Comando | Descrição |
|---|---|
| `npm run dev` | Servidor de desenvolvimento |
| `npm run build` | Build de produção |
| `npx vitest` | Rodar testes (watch mode) |
| `npx vitest run` | Rodar testes (single run) |
| `npx eslint src/` | Verificar lint |
| `npx tsc --noEmit` | Type check |

### Docker

| Comando | Descrição |
|---|---|
| `docker compose -f compose.dev.yml up --build` | Subir tudo (reconstruindo imagens) |
| `docker compose -f compose.dev.yml up db` | Subir apenas o banco |
| `docker compose -f compose.dev.yml down` | Parar tudo |
| `docker compose -f compose.dev.yml down -v` | Parar tudo e apagar volumes (dados) |

## Estrutura do Projeto

```
atividade_aps_p2/
├── backend/              # Django + DRF (Clean Architecture)
│   ├── apps/             # Bounded contexts (accounts, organizations, publications, chat)
│   ├── config/           # Django settings (base, development, production)
│   └── core/             # Shared kernel (base classes, exceptions, env)
├── frontend/             # React + TypeScript + TailwindCSS + Tanstack
│   └── src/
│       ├── app/          # Router, query client, App component
│       ├── features/     # Feature modules (auth, publications, etc.)
│       └── shared/       # Shared components, hooks, utilities
├── docker/               # Dockerfiles por serviço
├── docs/                 # Documentação detalhada
├── .github/              # GitHub Actions workflows
├── compose.dev.yml       # Docker Compose para desenvolvimento
└── compose.yml           # Docker Compose para produção
```

## Variáveis de Ambiente

Em desenvolvimento, **nenhuma variável de ambiente é obrigatória** — o sistema usa defaults seguros que funcionam com o `compose.dev.yml`.

Veja [docs/deployment/environment.md](../deployment/environment.md) para a lista completa de variáveis (obrigatórias e opcionais) em produção.
