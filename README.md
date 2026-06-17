# PetAdopt

PetAdopt é uma plataforma de adoção de animais com frontend React separado do backend Django. O objetivo é suportar um sistema de publicação de pets, organizações e comunicação entre interessados e publicantes com uma arquitetura limpa e deploy em Docker.

## O problema

A solução busca resolver a necessidade de organizar a adoção de animais de forma moderna, com:

- frontend interativo em SPA separado do backend
- backend API REST escalável e testável
- separação clara de responsabilidade entre serviços
- infraestrutura pronta para produção com Docker

## Estrutura da solução

O repositório é organizado como um monorepo com três camadas principais:

- `backend/` — Django + DRF, API, regras de negócio e configuração de ambiente
- `frontend/` — React + Vite + TypeScript + Tailwind, interface do usuário
- `docker/` — Dockerfiles para backend e frontend, scripts de entrypoint

Além disso há:

- `compose.dev.yml` — compose para desenvolvimento
- `compose.yml` — compose para produção
- `.env.example` — exemplo de variáveis de ambiente
- `.github/workflows/build.yml` — CI para build e publicação de imagens Docker

## Arquitetura e decisões técnicas

### Microsserviços e separação

A solução foi organizada como serviços independentes:

- `backend` roda o Django REST API
- `frontend` roda um build estático servido por Nginx no modo de produção
- `db` é PostgreSQL em container

Essa divisão facilita deploys independentes, testes de contrato e evolução futura de cada parte.

### Arquitetura Limpa

O backend segue a ideia de Clean Architecture com separação entre:

- `backend/core/` — abstrações de domínio e infra (ex: `backend/core/base_repository.py`, `backend/core/base_use_case.py`)
- `backend/apps/*/domain/` — entidades e interfaces de repositório por domínio
- `backend/apps/*/application/` — casos de uso, DTOs, comandos e observers
- `backend/apps/*/presentation/` — views, serializers e rotas expostas pela API
- `backend/config/` — settings por ambiente (`development.py`, `production.py`)

No frontend, a organização também é feature-based, com `frontend/src/features/` para cada domínio e `frontend/src/shared/` para componentes e hooks reutilizáveis.

### Princípios SOLID

A implementação atual e o plano adotam SOLID:

- **Single Responsibility** — componentes e use cases têm responsabilidade única
- **Open/Closed** — a arquitetura permite estender comportamento sem modificar elementos centrais
- **Liskov Substitution** — repositórios e interfaces podem ser substituídos por implementações de teste
- **Interface Segregation** — interfaces específicas por caso de uso
- **Dependency Inversion** — camadas altas dependem de abstrações, não de implementações concretas

### Design Patterns

A solução já evidencia padrões concretos no código:

- **Repository** — abstrata as operações de dados em `backend/core/base_repository.py` e em interfaces como `backend/apps/organizations/domain/repositories.py`.
- **Factory** — a criação de `PublicationEntity` e `PetEntity` é centralizada em `backend/apps/publications/domain/factories.py`.
- **Facade / Application Services** — os casos de uso em `backend/apps/*/application/use_cases/*.py` seguem a ideia de Application Services para orquestrar regras de negócio.
- **Strategy** — upload de arquivos no backend usa `backend/apps/organizations/application/strategies.py` e `backend/apps/publications/application/strategies.py`.
- **Observer** — auditoria de eventos da organização é implementada em `backend/apps/organizations/application/observers.py`.
- **Command** — ações administrativas estão em `backend/apps/organizations/application/commands.py`, como `ApproveOrganizationCommand` e `RejectOrganizationCommand`.

A arquitetura também está preparada para o uso de padrões adicionais como Adapter, em especial na camada `backend/apps/*/infrastructure/`, caso sejam necessárias integrações externas.

## Clean Code e boas práticas

Evidências do cuidado com qualidade:

- `backend/core/base_repository.py` e `backend/core/base_use_case.py` definem abstrações de repositório e use cases.
- `backend/apps/organizations/domain/repositories.py` e `backend/apps/publications/domain/factories.py` mostram a separação de camadas e responsabilidade única.
- `backend/apps/organizations/application/commands.py` e `backend/apps/organizations/application/observers.py` isolam lógica de comando e eventos.
- `backend/pyproject.toml` já contém configuração de `ruff`, `mypy` e `pytest`.
- `frontend/package.json` expõe `lint`, `build`, `dev` e `preview`.
- Todos os serviços Docker usam builds multi-stage e arquivos de ignore apropriados.
- `.env.example` documenta as variáveis de ambiente necessárias.
- `compose.yml` separa claramente o backend, frontend e banco de dados.

## Testes e validação

O projeto está preparado para testar com:

- backend: `pytest` via `pyproject.toml`
- frontend: `vitest` e ESLint via `package.json`

O repositório já contém testes TDD e BDD em arquivos como:

- `backend/apps/accounts/tests/unit/test_register_user.py`
- `backend/apps/organizations/tests/unit/test_organizations.py`
- `backend/apps/chat/tests/unit/test_chat_use_cases.py`
- `backend/apps/accounts/tests/features/authentication.feature`
- `backend/apps/organizations/tests/features/organization_workflow.feature`

Exemplos:

```bash
cd backend
pytest

cd ../frontend
npm run build
npm run lint
npx vitest run
```

O arquivo `frontend/package.json` já contém o script `build` e dependências de teste.

## Configuração do ambiente

Copie o exemplo de ambiente para `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Ajuste os valores obrigatórios:

- `SECRET_KEY`
- `POSTGRES_PASSWORD`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`

O arquivo `.env.example` inclui o mínimo necessário para deploy local com Docker.

### Rodando em modo de produção local

```bash
docker compose -f compose.yml up -d --build
```

Verifique os serviços:

```bash
docker compose -f compose.yml ps
```
