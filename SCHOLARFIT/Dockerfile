FROM nginx:1.27.2-alpine

RUN rm -rf /usr/share/nginx/*
COPY . /usr/share/nginx/html

RUN chown -R nginx:nginx /usr/share/nginx/html && chmod -R 755 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

