# Credentials Setup för PyPI Upload

Denna guide visar hur du konfigurerar autentisering för att ladda upp pip-paketet till den privata GitLab PyPI-repositoryn.

## 📁 Skapa mina-credentials.txt

Skapa filen `build-pip/mina-credentials.txt` med följande innehåll:

```bash
# Mina GitLab credentials för PyPI upload
# Uppdatera dessa värden med dina riktiga uppgifter

GITLAB_USERNAME=din_gitlab_username
GITLAB_TOKEN=din_gitlab_token
```

## 🔑 Så här får du dina GitLab credentials

### 1. GitLab Username
- Ditt GitLab användarnamn (t.ex. `per.nehlin`)

### 2. GitLab Access Token
Följ dessa steg för att skapa en access token:

1. **Logga in på GitLab**
   - Gå till https://git.idp.ip-solutions.se
   - Logga in med dina credentials

2. **Gå till Access Tokens**
   - Klicka på din profilbild (övre högra hörnet)
   - Välj "Settings" eller "Inställningar"
   - Klicka på "Access Tokens" i vänstra menyn

3. **Skapa ny token**
   - Fyll i "Token name" (t.ex. "PyPI Upload")
   - Välj "Expiration date" (rekommenderat: 1 år)
   - **Viktigt:** Kryssa i `write_repository` under "Scopes"
   - Klicka "Create personal access token"

4. **Kopiera token**
   - **Viktigt:** Kopiera token direkt - du kan inte se den igen!
   - Token börjar oftast med `glpat-`

## ✅ Exempel på komplett fil

Här är ett exempel på hur din `mina-credentials.txt` ska se ut:

```bash
# Mina GitLab credentials för PyPI upload
# Uppdatera dessa värden med dina riktiga uppgifter

GITLAB_USERNAME=per.nehlin
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
```

## 🚀 Användning

När du har skapat filen med dina riktiga credentials:

```bash
# Bygg och ladda upp paketet
./scripts/build-pip.sh build upload

# Eller bara ladda upp om paketet redan är byggt
./scripts/build-pip.sh upload
```

## 🔒 Säkerhet

- `mina-credentials.txt` är redan tillagd i `.gitignore`
- Filen kommer INTE att committas till Git
- Håll din access token säker och dela den inte med andra
- Om token läcker, återkalla den direkt i GitLab

## ❌ Vanliga fel

### "mina-credentials.txt innehåller inte giltiga credentials!"
- Kontrollera att du har uppdaterat `GITLAB_USERNAME` och `GITLAB_TOKEN`
- Se till att du inte har kvar exempel-värdena

### "401 Unauthorized"
- Kontrollera att din access token är giltig
- Se till att token har `write_repository` scope
- Kontrollera att användarnamnet är korrekt

### "Repository not found"
- Kontrollera att repository URL:en är korrekt
- Kontrollera att du har tillgång till projektet

## 🔄 Återkalla token

Om din token läcker eller du vill skapa en ny:

1. Gå till GitLab > Settings > Access Tokens
2. Hitta din token i listan
3. Klicka "Revoke" för att återkalla den
4. Skapa en ny token enligt stegen ovan
5. Uppdatera `mina-credentials.txt` med den nya token
