# syntax=docker/dockerfile:1.6

FROM node:20-bookworm as deps
WORKDIR /app
COPY package.json ./
RUN corepack enable pnpm && pnpm install

FROM node:20-bookworm as builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN corepack enable pnpm && pnpm build

FROM node:20-bookworm-slim as runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./package.json
EXPOSE 3000
CMD ["node", "node_modules/next/dist/bin/next", "start"]
