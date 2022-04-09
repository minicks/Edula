FROM node:16.13-alpine as builder
WORKDIR /app/frontend
COPY ./frontend .
RUN npm i -g npm@latest
RUN npm i
RUN npm run build

FROM nginx:latest
RUN rm -rf /etc/nginx/conf.d
COPY --from=builder /app/frontend/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]