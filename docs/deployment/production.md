# Deploy de produção

Este guia descreve o deploy da stack de produção usando `docker compose`.

## Preparação

1. Crie um arquivo de ambiente ou exporte as variáveis necessárias.
2. Garanta que `SECRET_KEY`, `POSTGRES_PASSWORD`, `ALLOWED_HOSTS` e `CORS_ALLOWED_ORIGINS` estejam definidos.

## Deploy com Docker Compose

No diretório raiz do projeto:

```bash
docker compose -f compose.yml up -d --build
```

Isso irá:

- construir as imagens de produção do backend e frontend;
- iniciar um container PostgreSQL;
- inicializar o backend e o frontend;
- expor o backend em `:8000` e o frontend em `:80`.

## Comandos de inspeção

Verifique o status dos serviços:

```bash
docker compose -f compose.yml ps
```

Veja os logs do backend:

```bash
docker compose -f compose.yml logs -f backend
```

## Atualização de versão

Após alteração do código ou de dependências:

```bash
docker compose -f compose.yml up -d --build
```

## Parando a stack

```bash
docker compose -f compose.yml down
```

## Observações

- O container do backend valida variáveis obrigatórias no startup e falha rapidamente quando alguma delas está ausente.
- Se a conexão com o banco de dados falhar, o backend aguardará até que o PostgreSQL esteja disponível antes de rodar as migrações.
