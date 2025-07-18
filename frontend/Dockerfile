# Stage 1: build
FROM node:alpine as build

COPY . .
RUN npm run build

# Stage 2: serve with nginx
FROM nginx:stable-alpine

# Копируем готовые статики
COPY --from=build /app/dist /usr/share/nginx/html


EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
