#######################################################################
# Stage 1 — builder: устанавливаем зависимости, генерируем TS-клиент,
#            собираем Next.js в production-режиме
#######################################################################
FROM node:24.5-alpine AS builder
WORKDIR /app

# 1. Устанавливаем prod+dev зависимости
COPY package*.json ./
# Используем npm ci если есть package-lock.json, иначе npm install с --legacy-peer-deps для совместимости
RUN if [ -f "package-lock.json" ]; then npm ci; else npm install --legacy-peer-deps; fi

# 2. Копируем исходники фронта
COPY . .

# 3. Создаем заглушку OpenAPI для разработки (в продакшене файл копируется в CI)
RUN echo '{"openapi":"3.0.0","info":{"title":"API","version":"1.0.0"},"paths":{}}' > ./openapi.json

# 4. Генерируем TypeScript-типы и fetch-клиент (заглушки для разработки)
RUN npx openapi-typescript ./openapi.json -o src/api/schema.ts || echo 'export type paths = {};' > src/api/schema.ts
RUN npx openapi-typescript-fetch --input ./openapi.json --output src/api/client.ts || echo 'export const api = {};' > src/api/client.ts

# 5. Production-сборка Next.js (используем output = standalone, если задано)
RUN npm run build

#######################################################################
# Stage 2 — final: минимальный образ для запуска
#######################################################################
FROM node:24.5-alpine AS final
WORKDIR /app
ENV NODE_ENV=production

# 6. Копируем артефакты сборки
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
#  └─ schema.ts и client.ts уже “запечены” внутрь .next-output

# 7. Ставим только prod-зависимости
RUN npm install --prod

# 8. Безопасный непривилегированный пользователь
RUN addgroup -g 1001 nodegrp && \
    adduser -D -G nodegrp -u 1001 nodeusr && \
    chown -R nodeusr /app
USER nodeusr

EXPOSE 3000
CMD ["npm", "start"]
