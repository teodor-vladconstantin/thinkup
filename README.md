# ThinkUp Platform

Acesta este repository-ul central pentru platforma **ThinkUp**. Proiectul este organizat ca un monorepo ce conține atât partea de frontend, cât și backend-ul și configurațiile de infrastructură (Docker).

## 📂 Structura Proiectului

- **`platform-frontend/`**: Aplicația web construită cu **Next.js**.
- **`platform-backend/`**: API-ul construit cu **Python Flask** și scripturile de bază de date.
- **`platform-backend/docker-compose.yml`**: Configurația principală pentru a rula toată infrastructura local.

## � Documentație

*   **[ONBOARDING.md](ONBOARDING.md)**: Ghid pentru programatori noi (cum să instalezi și să rulezi local).
*   **[DEPLOY_VPS.md](DEPLOY_VPS.md)**: Ghid pentru migrarea pe server de producție (VPS Hostico/AWS/etc).

## �🚀 Cum să rulezi proiectul (Docker)

Cea mai simplă metodă de a porni aplicația este folosind Docker Compose.

### 1. Prerechi
Asigură-te că ai instalat [Docker Desktop](https://www.docker.com/products/docker-desktop/) pe mașina ta.

### 2. Configurare Variabile de Mediu (Frontend)
Înainte de a porni, frontend-ul are nevoie de cheile de autentificare Auth0.

1. Intră în folderul `platform-frontend`.
2. Creează un fișier numit `.env.local` (copiază exemplul din `.env.example`).
3. Completează variabilele necesare:

```bash
# platform-frontend/.env.local

AUTH0_SECRET='...'           # Generează cu `openssl rand -hex 32`
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='...'  # Domeniul tău Auth0
AUTH0_CLIENT_ID='...'        # Client ID din Auth0
AUTH0_CLIENT_SECRET='...'    # Client Secret din Auth0
NEXT_PUBLIC_API_URL='http://localhost' # URL-ul API-ului (prin Nginx/Docker)
```

### 3. Pornire Platformă

Deschide un terminal în rădăcina proiectului și rulează:

```bash
# Intră în folderul backend unde se află configurația Docker
cd platform-backend

# Pornește containerele (Frontend + Backend + ScyllaDB + Nginx)
docker-compose up --build -d
```

### 4. Accesare

Odată ce containerele sunt "Up" (poate dura câteva minute prima dată pentru inițializarea bazei de date ScyllaDB):

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **API (Direct)**: [http://localhost:5000](http://localhost:5000)
- **API (Prin Nginx)**: [http://localhost/api](http://localhost/api)

## 🛠 Comenzi Utile

**Oprire servere:**
```bash
docker-compose down
```

**Vizualizare log-uri:**
```bash
docker-compose logs -f
```

**Migrare/Inițializare Bază de Date (dacă e necesar manual):**
Dacă baza de date nu se populează automat, poți rula scripturile din `platform-backend`.
```bash
# Exemplu (din interiorul containerului backend sau local cu venv activat)
python init_local_db.py
```
