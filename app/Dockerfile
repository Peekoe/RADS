FROM node:18-alpine AS build

RUN apk update
RUN apk add git
RUN git clone https://github.com/Peekoe/RADS.git

WORKDIR /RADS/app
RUN npm install
RUN npm run build

FROM nginx:1.23.3-alpine-slim AS deploy-static

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build RADS/app/dist .
ENTRYPOINT ["nginx", "-g", "daemon off;"]