FROM node:18-alpine AS build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

FROM nginx:1.23.3-alpine-slim AS deploy-static

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/dist .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
