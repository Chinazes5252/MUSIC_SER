# Stage 1: build
FROM node:16-alpine as build
WORKDIR /app

# Копируем только описание зависимостей
COPY package.json package-lock.json ./

# Устанавливаем их (npm ci чище и детерминированнее)
RUN npm ci

# Копируем весь остальной код
COPY . .

# Собираем статический сайт
RUN npm run build

# Stage 2: serve with nginx
FROM nginx:stable-alpine
# Статические файлы из /app/dist
COPY --from=build /app/dist /usr/share/nginx/html
# Конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
