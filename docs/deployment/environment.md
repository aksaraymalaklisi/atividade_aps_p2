# Variáveis de ambiente de produção

O backend de produção requer variáveis de ambiente para segurança e conectividade com o banco de dados.

## Obrigatórias

- `SECRET_KEY`
  - Chave secreta Django para assinaturas e criptografia.
- `POSTGRES_PASSWORD`
  - Senha do usuário PostgreSQL.
- `ALLOWED_HOSTS`
  - Lista separada por vírgulas com hosts permitidos.
  - Exemplo: `petadopt.example.com,api.petadopt.example.com`
- `CORS_ALLOWED_ORIGINS`
  - Lista separada por vírgulas com origens permitidas para o frontend.
  - Exemplo: `https://petadopt.example.com`

## Recomendadas/Com defaults

- `POSTGRES_DB`
  - Banco de dados PostgreSQL.
  - Default: `petadopt`
- `POSTGRES_USER`
  - Usuário PostgreSQL.
  - Default: `postgres`
- `POSTGRES_HOST`
  - Host do serviço PostgreSQL.
  - Default: `db`
- `POSTGRES_PORT`
  - Porta do PostgreSQL.
  - Default: `5432`
- `SENTRY_DSN`
  - DSN do Sentry para monitoramento de erros.
  - Opcional.

## Exemplo de `.env`

O repositório também inclui um arquivo de referência de variáveis de ambiente em `.env.example`.
Copie-o para `.env` e ajuste os valores antes de executar o deploy.

```env
SECRET_KEY=changeme1234567890
POSTGRES_PASSWORD=postgres
ALLOWED_HOSTS=petadopt.example.com
CORS_ALLOWED_ORIGINS=https://petadopt.example.com
POSTGRES_DB=petadopt
POSTGRES_USER=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
