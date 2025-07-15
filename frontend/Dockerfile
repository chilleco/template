# Stage 1: builder – собираем Next.js проект
FROM node:18-alpine AS builder
WORKDIR /app

# Установим зависимости
COPY package*.json ./
RUN npm ci         # устанавливаем все пакеты (включая devDependencies, нужные для сборки)

COPY . .           # копируем весь исходный код фронтенда
RUN npm run build  # выполняем сборку Next.js (пререндер/бандлинг)

# Stage 2: final – запуск оптимизированного сборки
FROM node:18-alpine AS final
WORKDIR /app

# Забираем только необходимые артефакты и зависимости
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next            # Next.js билд (пререндеренные страницы, статика, серверные бандлы)
COPY --from=builder /app/public ./public          # публичные файлы
COPY --from=builder /app/package.json ./package.json

# Устанавливаем только production-зависимости (для запуска Next.js сервера)
RUN npm install --prod

# (Опционально: можно удалить переменные, скрипты сборки и dev-зависимости, если они всё еще подтянулись)

# Создаём пользователя
RUN addgroup -g 1001 nodegrp && adduser -D -G nodegrp -u 1001 nodeusr && chown -R nodeusr /app
USER nodeusr

EXPOSE 3000
CMD ["npm", "start"]   # запускаем Next.js в режиме production (next start)
