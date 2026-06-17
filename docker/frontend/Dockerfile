# =============================================================================
# PetAdopt Frontend — Multi-stage Dockerfile
# =============================================================================

# --- Stage: development ---
FROM node:24-alpine AS development

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 5173

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# --- Stage: build ---
FROM node:24-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
# Allow injecting the frontend API base at build time (Vite reads VITE_* env vars)
ARG VITE_API_URL
ARG VITE_BACKEND_BASE
ENV VITE_API_URL=${VITE_API_URL}
ENV VITE_BACKEND_BASE=${VITE_BACKEND_BASE}

RUN npm run build

# --- Stage: production ---
FROM nginx:alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:80/ || exit 1
