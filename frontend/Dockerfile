# Enkel React frontend med serve
FROM node:18-alpine

WORKDIR /app

# Installera serve globalt
RUN npm install -g serve

# Kopiera package files
COPY package*.json ./

# Installera alla dependencies (inklusive dev dependencies för build)
RUN npm install

# Kopiera källkod
COPY . .

# Bygg applikationen
RUN npm run build

# Exponera port
EXPOSE 3000

# Starta serve för att servera byggda filer
CMD ["serve", "-s", "dist", "-l", "3000"]
