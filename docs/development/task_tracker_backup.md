# PetAdopt Refatoração — Task Tracker

## Fase 1 — Fundação do Projeto ✅

- [x] Criar estrutura monorepo (`backend/`, `frontend/`, `docs/`, `docker/`)
- [x] Inicializar backend Django com Clean Architecture skeleton
  - [x] Criar projeto Django em `backend/` com `config` como projeto
  - [x] Split de settings (base, development, production)
  - [x] Criar apps skeleton (accounts, organizations, publications, chat)
  - [x] Criar domain/application/infrastructure/presentation em cada app
  - [x] Criar core shared kernel (base_entity, base_repository, base_use_case, exceptions, env)
  - [x] Configurar requirements (base, development, production)
  - [x] Configurar pyproject.toml (ruff, pytest)
  - [x] Re-exportar modelos ORM via `models.py` no nível do app (bridge para Clean Architecture)
- [x] Inicializar frontend React + Vite + TailwindCSS + Tanstack
  - [x] Scaffold com Vite (React + TypeScript)
  - [x] Configurar TailwindCSS 4
  - [x] Instalar e configurar Tanstack Router + Query
  - [x] Criar estrutura de features (auth, publications, organizations, chat, operator)
  - [x] Configurar vitest
- [x] Configurar Docker multi-stage (dev + prod)
  - [x] Backend Dockerfile (multi-stage: base + development + production)
  - [x] Frontend Dockerfile (multi-stage: development + build + production)
  - [x] compose.dev.yml com PostgreSQL
  - [x] .dockerignore para backend e frontend
- [x] Criar GitHub Actions workflow básico (lint + test)
- [x] Documentar setup em `docs/development/setup.md`
- [x] Verificar backend: Django check ✅, makemigrations ✅, migrate ✅, User model ✅
- [x] Verificar frontend: tsc --noEmit ✅, vite build ✅

> **Nota:** Pillow atualizado para >=11.0 por compatibilidade com Python 3.14.

## Fase 2 — Usuários & Autenticação
- [x] Implementar domain entities (User) — skeleton já criado
- [x] Implementar repositórios (interface + Django ORM)
- [x] Implementar use cases (Register, Login, Profile)
- [x] Implementar API endpoints (DRF) + JWT
- [x] Implementar frontend auth flow (Login, Register, Protected Routes)
- [x] TDD: testes unitários para cada use case
- [x] BDD: cenários de registro e login

## Fase 3 — Organizações
- [ ] (pendente)

## Fase 4 — Publicações & Pets
- [ ] (pendente)

## Fase 5 — Chat
- [ ] (pendente)

## Fase 6 — CI/CD & Produção
- [ ] (pendente)

## Fase 7 — Documentação & Polish
- [ ] Polir Interface (Adicionar Dark Mode e refinar Glassmorphism e estilos globais)
- [ ] Documentação final
