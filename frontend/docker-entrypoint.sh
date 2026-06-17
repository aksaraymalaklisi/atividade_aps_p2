#!/bin/sh

# Verifica se o package.json foi modificado e as dependências precisam ser instaladas
# Executa npm install de forma silenciosa para sincronizar o volume anônimo
echo "Verificando dependências do Node (sync de volume local)..."
npm install --no-fund --no-audit

# Executa o comando passado para o container (ex: npm run dev)
exec "$@"
