# Enkel React frontend med serve
FROM node:18-alpine

WORKDIR /app

# Installera serve globalt
RUN npm install -g serve

# Kopiera färdigbyggda dist-mappen från build-npm
COPY dist/ ./dist/

# Exponera port
EXPOSE 3000

# Starta serve för att servera byggda filer med SPA-support
CMD ["serve", "-s", "dist", "-l", "3000"]
