# 📅 Schemaläggare API

Schemaläggaren låter dig automatisera API-anrop genom att skapa scheman som körs enligt specifika tidsintervall. Detta är perfekt för att hämta data regelbundet, synkronisera system eller köra underhållsuppgifter.

## 🚀 Funktioner

- **Flexibel schemaläggning**: Daglig, veckovis, månadsvis eller engångskörning
- **Anpassningsbara endpoints**: Kör vilken API-endpoint som helst
- **HTTP-metoder**: Stöd för GET, POST, PUT, DELETE
- **Headers och data**: Skicka anpassade headers och request body
- **Aktivering/inaktivering**: Enkelt att pausa och återuppta scheman
- **Körningshistorik**: Spåra alla körningar och deras resultat
- **Maximalt antal körningar**: Begränsa hur många gånger ett schema ska köras

## 📋 API Endpoints

### Hämta alla scheman
```bash
curl -X GET http://localhost:8000/api/schedule/
```

### Skapa ett nytt schema
```bash
curl -X POST http://localhost:8000/api/schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daglig hälsokontroll",
    "endpoint": "/api/health",
    "method": "GET",
    "frequency": "daily",
    "start_time": "2025-09-26T12:00:00Z"
  }'
```

### Hämta specifikt schema
```bash
curl -X GET http://localhost:8000/api/schedule/{schedule_id}
```

### Uppdatera schema
```bash
curl -X PUT http://localhost:8000/api/schedule/{schedule_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Uppdaterat schema",
    "frequency": "weekly"
  }'
```

### Ta bort schema
```bash
curl -X DELETE http://localhost:8000/api/schedule/{schedule_id}
```

### Köra schema manuellt
```bash
curl -X POST http://localhost:8000/api/schedule/{schedule_id}/execute
```

### Aktivera schema
```bash
curl -X POST http://localhost:8000/api/schedule/{schedule_id}/enable
```

### Inaktivera schema
```bash
curl -X POST http://localhost:8000/api/schedule/{schedule_id}/disable
```

### Hämta körningshistorik
```bash
curl -X GET http://localhost:8000/api/schedule/{schedule_id}/executions
```

## 📝 Schema-konfiguration

### Obligatoriska fält
- `name`: Namn på schemat (sträng)
- `endpoint`: API-endpoint att anropa (måste börja med `/`)
- `method`: HTTP-metod (`GET`, `POST`, `PUT`, `DELETE`)
- `frequency`: Körningsfrekvens (`once`, `daily`, `weekly`, `monthly`, `custom`)

### Valfria fält
- `headers`: Anpassade HTTP-headers (objekt)
- `data`: Request body för POST/PUT (objekt)
- `start_time`: När schemat ska börja köras (ISO 8601 datum)
- `end_time`: När schemat ska sluta köras (ISO 8601 datum)
- `max_executions`: Maximalt antal körningar (nummer)
- `cron_expression`: Anpassad cron-uttryck för `custom` frekvens
- `enabled`: Om schemat är aktiverat (boolean, standard: true)

## 💡 Exempel

### 1. Daglig hälsokontroll
```bash
curl -X POST http://localhost:8000/api/schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daglig hälsokontroll",
    "endpoint": "/api/health",
    "method": "GET",
    "frequency": "daily",
    "start_time": "2025-09-26T09:00:00Z"
  }'
```

### 2. Veckovis hämta repositories
```bash
curl -X POST http://localhost:8000/api/schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Veckovis repository-synkronisering",
    "endpoint": "/api/repositories/",
    "method": "GET",
    "frequency": "weekly",
    "start_time": "2025-09-26T08:00:00Z",
    "max_executions": 52
  }'
```

### 3. Månadsvis skapa backup
```bash
curl -X POST http://localhost:8000/api/schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Månadsvis backup",
    "endpoint": "/api/packages/",
    "method": "POST",
    "frequency": "monthly",
    "start_time": "2025-09-26T02:00:00Z",
    "headers": {
      "Authorization": "Bearer your-token",
      "Content-Type": "application/json"
    },
    "data": {
      "backup_type": "full",
      "destination": "s3://backup-bucket"
    }
  }'
```

### 4. Engångskörning
```bash
curl -X POST http://localhost:8000/api/schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engångs-migration",
    "endpoint": "/api/repositories/",
    "method": "POST",
    "frequency": "once",
    "start_time": "2025-09-26T15:30:00Z",
    "data": {
      "migration_type": "data_cleanup"
    }
  }'
```

### 5. Anpassat schema med cron
```bash
curl -X POST http://localhost:8000/api/schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Varje vardag kl 14:30",
    "endpoint": "/api/health",
    "method": "GET",
    "frequency": "custom",
    "cron_expression": "30 14 * * 1-5",
    "start_time": "2025-09-26T14:30:00Z"
  }'
```

## 🔄 Schema-status

### Aktiva scheman
Scheman som är `enabled: true` och har en framtida `next_execution` tid.

### Pausade scheman
Scheman som är `enabled: false` eller har passerat `end_time`.

### Slutförda scheman
Scheman med `frequency: "once"` som har körts, eller scheman som har nått `max_executions`.

## 📊 Körningshistorik

Varje schema-körning sparas med följande information:
- `executed_at`: När körningen skedde
- `status`: Körningsstatus (`running`, `completed`, `failed`)
- `response_status`: HTTP-statuskod från API:et
- `response_data`: Svar från API:et
- `error_message`: Felmeddelande om körningen misslyckades
- `execution_time_ms`: Hur lång tid körningen tog

## ⚠️ Begränsningar

- **In-memory storage**: Scheman sparas i minnet och försvinner vid omstart
- **Ingen persistence**: Körningshistorik sparas inte permanent
- **Enkel cron**: Anpassade cron-uttryck är begränsade
- **Ingen retry-logik**: Misslyckade körningar försöks inte igen automatiskt

## 🛠️ Felsökning

### Schema körs inte
1. Kontrollera att schemat är `enabled: true`
2. Verifiera att `start_time` har passerat
3. Kolla att `end_time` inte har passerat
4. Kontrollera att `max_executions` inte har nåtts

### API-anrop misslyckas
1. Verifiera att endpoint:en existerar
2. Kontrollera HTTP-metod
3. Kolla headers och data-format
4. Titta på körningshistorik för felmeddelanden

### Schema försvinner
1. Scheman sparas i minnet - de försvinner vid omstart
2. Använd `GET /api/schedule/` för att se aktiva scheman

## 🔗 Relaterade länkar

- [Huvud-README](../../README.md)
- [API-dokumentation](http://localhost:8000/api/docs)
- [Swagger UI](http://localhost:8000/api/docs)
