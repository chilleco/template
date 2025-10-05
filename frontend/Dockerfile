FROM node:20-alpine

WORKDIR /app
COPY package.json package-lock.json* tsconfig.json .eslintrc.json .prettierrc tailwind.config.ts postcss.config.js next.config.mjs vitest.config.ts vitest.setup.ts ./
COPY app ./app
COPY src ./src
COPY scripts ./scripts
COPY schema ./schema

RUN npm install --legacy-peer-deps
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "dev"]
