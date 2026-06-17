# Docker em produção

Este arquivo descreve a arquitetura de contêineres usada em produção para a plataforma PetAdopt.

## Visão geral

A configuração de produção usa `compose.yml` para orquestrar três serviços:

- `db`: PostgreSQL 16 para persistência de dados.
- `backend`: API Django em modo `production` com Gunicorn.
- `frontend`: SPA React servida pelo Nginx.

O backend roda com imagens construídas a partir de `docker/backend/Dockerfile` e o frontend a partir de `docker/frontend/Dockerfile`.

## Como funciona

- O `backend` utiliza `backend/config/settings/production.py` e valida variáveis de ambiente obrigatórias no startup.
- O `backend` executa migrações e coleta arquivos estáticos automaticamente antes de iniciar o servidor.
- O `frontend` serve a aplicação compilada em `dist/` por meio do Nginx, com suporte a rotas de SPA.

## Comandos úteis

```bash
docker compose -f compose.yml build
docker compose -f compose.yml up -d
```

Para ver os logs de um serviço:

```bash
docker compose -f compose.yml logs -f backend
```

Para parar a stack:

```bash
docker compose -f compose.yml down
```
