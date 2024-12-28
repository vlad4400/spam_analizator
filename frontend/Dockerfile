# frontend/Dockerfile

# Obraz bazowy do budowania Angulara
FROM node:18 as build-stage

WORKDIR /app

# Skopiuj package.json i package-lock.json (jeśli istnieje)
COPY package*.json ./

# Zainstaluj zależności
RUN npm install

# Skopiuj pozostałe pliki źródłowe Angular
COPY . .

# Zbuduj aplikację Angular
RUN npm run build --prod

# Drugi stage - serwer (np. użyjemy Nginx do hostowania buildu)
FROM nginx:stable-alpine as production-stage

# Skopiuj z poprzedniego stage pliki z dist/ do /usr/share/nginx/html
COPY --from=build-stage /app/dist/frontend/browser /usr/share/nginx/html

# Otwórz port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
