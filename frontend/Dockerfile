# просто берем чистый nginx
FROM nginx:stable-alpine

# копируем все статические файлы в директорию Nginx
COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
