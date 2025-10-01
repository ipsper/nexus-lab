# Nexus Repository Frontend

En modern React frontend för Nexus Repository Manager API, designad med inspiration från [IP-Solutions](https://www.ip-solutions.se/) webbplats.

## 🚀 Snabbstart

### Förutsättningar

- Node.js 18+ 
- npm eller yarn
- Kind-kluster med Nexus Repository Manager API

### Installation

```bash
# Installera dependencies
npm install

# Starta utvecklingsserver
npm run dev
```

Frontend kommer att vara tillgänglig på `http://localhost:3000`

## 🏗️ Bygga som npm-paket

```bash
# Bygga som bibliotek
npm run build:lib

# Bygga för produktion
npm run build
```

## 🔧 Konfiguration

### Miljövariabler

Skapa en `.env.local` fil:

```env
VITE_API_URL=http://localhost:8000/api
```

### API-proxy

Utvecklingsservern är konfigurerad att proxya `/api` requests till backend-servern.

## 📁 Projektstruktur

```
frontend/
├── src/
│   ├── components/          # Återanvändbara komponenter
│   │   ├── ui/             # Grundläggande UI-komponenter
│   │   ├── dashboard/      # Dashboard-specifika komponenter
│   │   ├── repositories/   # Repository-hantering
│   │   ├── schedules/      # Schema-hantering
│   │   └── layout/         # Layout-komponenter
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API-tjänster
│   ├── types/              # TypeScript-typer
│   ├── pages/              # Sidor/routes
│   └── App.tsx             # Huvudapplikation
├── public/                 # Statiska filer
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## 🎨 Design

Frontend använder:
- **React 18** med TypeScript
- **Tailwind CSS** för styling
- **Lucide React** för ikoner
- **React Query** för datahantering
- **React Router** för navigation

Designen är inspirerad av IP-Solutions webbplats med:
- Professionell blå färgschema
- Ren, modern layout
- Responsiv design
- Hover-effekter och animationer

## 🔌 API-integration

Frontend kommunicerar med FastAPI backend via:
- Health checks (`/api/health`)
- Repository management (`/api/repositories/`)
- Schedule management (`/api/schedule/`)
- Statistics (`/api/stats`)
- Configuration (`/api/config`)

## 📱 Responsiv design

- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Anpassad navigation för mobil

## 🧪 Utveckling

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Preview production build
npm run preview
```

## 📦 Deployment

### Som npm-paket

```bash
npm run build:lib
# Distribuera dist/ mappen
```

### Som standalone app

```bash
npm run build
# Distribuera dist/ mappen till webbserver
```

## 🔗 Länkar

- [Backend API Documentation](../build-pip/nexus_repository_api/README.md)
- [Kind Setup Guide](../README.md)
- [IP-Solutions Inspiration](https://www.ip-solutions.se/)
