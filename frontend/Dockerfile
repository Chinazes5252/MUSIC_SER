# Stage 1: build
FROM node:16-alpine as build
WORKDIR /app


RUN npm ci

# Копируем весь остальной код и собираем
COPY . .
RUN npm run build

# Stage 2: serve with nginx
FROM nginx:stable-alpine

# Копируем готовые статики
COPY --from=build /app/dist /usr/share/nginx/html

# (Убираем COPY nginx.conf — не нужен)
# Если хочешь свой конфиг, положи его в frontend/nginx.conf и раскомментируй:
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
