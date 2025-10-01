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

# Kopiera serve.json till dist-mappen
RUN cp serve.json dist/ || echo "serve.json finns inte, fortsätter ändå"

# Exponera port
EXPOSE 3000

# Starta serve för att servera byggda filer med SPA-support
CMD ["serve", "-s", "dist", "-l", "3000"]
