FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
# Use npm install to allow lock refresh in case dependencies drift; npm ci was failing on mismatch.
RUN npm install

COPY . .
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

FROM nginx:1.27-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
