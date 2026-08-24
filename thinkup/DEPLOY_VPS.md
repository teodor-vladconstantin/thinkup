# 🌐 Ghid de Migrare pe VPS (Hostico, DigitalOcean, AWS, etc.)

Acest ghid explică pas cu pas cum să muți aplicația ThinkUp de pe dezvoltare locală pe un server de producție (VPS).

---

## 🏗️ 1. Pregătirea Serverului (VPS)

Presupunem că ai cumpărat un VPS de la Hostico (sau alt furnizor) și ai primit datele de acces (IP și Root Password). Sistemul de operare recomandat este **Ubuntu 22.04 LTS** sau **20.04 LTS**.

### 1.1 Conectează-te la VPS
Deschide un terminal (PowerShell sau CMD pe Windows) și rulează:
```bash
ssh root@<ip-ul-tau-vps>
# Exemplu: ssh root@89.123.45.67
```
*Introdu parola când ți se cere (nu se va vedea pe ecran când tastezi).*

### 1.2 Instalează Docker și Git
Odată conectat pe server, rulează aceste comenzi pentru a instala tot ce e necesar:

```bash
# Actualizează sistemul
apt update && apt upgrade -y

# Instalează Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalează Docker Compose (dacă nu s-a instalat automat)
apt install docker-compose-plugin -y
```

---

## 📥 2. Instalarea Aplicației

### 2.1 Clonează Repository-ul
Deoarece repository-ul este privat, vei avea nevoie de un **Personal Access Token (PAT)** GitHub sau să folosești SSH Keys. Varianta cu HTTPS + Token e cea mai simplă pe moment.

```bash
# Clonează proiectul
git clone https://github.com/teodor-vladconstantin/thinkup.git

# Intră în folder
cd thinkup/platform-backend
```
*Când îți cere parola de GitHub, introdu Token-ul, nu parola contului tău.*

### 2.2 Configurează Secretele (.env)
Trebuie să creezi fișierul cu variabilele secrete pentru frontend (Auth0).

```bash
# Mergi la frontend
cd ../platform-frontend

# Creează fișierul .env.local
nano .env.local
```

Lipește conținutul fișierului tău local `.env.local` (Auth0 Secret, Client ID, etc.).

⚠️ **IMPORTANT PENTRU PRODUCȚIE:**
Caută linia `AUTH0_BASE_URL` și schimb-o din `http://localhost:3000` în adresa site-ului tău real:
```properties
AUTH0_BASE_URL=https://domeniul-tau.ro
```
*Dacă o lași pe localhost, login-ul nu va merge!*

*   Apasă `Ctrl+O` apoi `Enter` pentru a salva.
*   Apasă `Ctrl+X` pentru a ieși.

---

## 🚀 3. Pornirea Aplicației

Înapoi în folderul de backend:
```bash
cd ../platform-backend

# Pornește serverele (în background)
docker compose up --build -d
```
Acum aplicația rulează pe portul 80 pe server!

---

## 💾 4. Restaurarea Datelor

Pe serverul nou, baza de date este goală. Vom folosi sistemul de seeding creat anterior pentru a importa datele.

```bash
docker exec -it thinkup-app python scripts/load_db_from_json.py
```
*Acesta va lua JSON-urile din folderul `seed_data` (care au venit prin Git) și le va băga în baza de date locală a VPS-ului.*

---

## 🔒 5. Conectarea la Domeniu (Cloudflare Tunnel)

Pentru a avea **HTTPS (lăcățelul verde)** automat și protecție anti-DDoS, recomandăm folosirea **Cloudflare**.

### 5.0 Prerechizite (Important)
1.  Domeniul tău (ex: `thinkup.ro`) cumpărat de la Hostico/RoTLD.
2.  Cont gratuit pe [Cloudflare](https://www.cloudflare.com/).
3.  **Schimbă Nameserverele:** Intră în panoul Hostico -> Domenii -> Nameservers și pune-le pe cele primite de la Cloudflare (ex: `adi.ns.cloudflare.com` si `bob.ns.cloudflare.com`).
4.  Așteaptă propagarea (1-2 ore).

### 5.1 Instalează Cloudflared pe VPS
```bash
# Descarcă pachetul
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Instalează
dpkg -i cloudflared-linux-amd64.deb
```

### 5.2 Creează Tunelul
1.  Loghează-te (vei primi un link în terminal, copiază-l în browser-ul tău de acasă):
    ```bash
    cloudflared tunnel login
    ```
2.  Creează tunelul:
    ```bash
    cloudflared tunnel create thinkup-production
    ```
3.  Leagă tunelul de domeniul tău (ex: app.thinkup.ro):
    ```bash
    # Înlocuiește cu numele tunelului și domeniul tău
    cloudflared tunnel route dns thinkup-production app.thinkup.ro
    ```
4.  Pornește tunelul:
    ```bash
    # Rutează traficul către Nginx (port 80)
    cloudflared tunnel run --url http://localhost:80 thinkup-production
    ```

💡 **Sfat Pro:** Pentru ca tunelul să rămână pornit și după ce închizi terminalul, instalează-l ca serviciu:
```bash
cloudflared service install <token-ul-tau-din-dashboard-cloudflare>
```
*(Token-ul îl iei din dashboard-ul Cloudflare Zero Trust -> Access -> Tunnels dacă vrei să faci asta din interfață, sau urmezi ghidul de CLI pentru servicii).*

---

## 🔑 6. Configurare Auth0 (Obligatoriu)

Chiar dacă ai setat `.env` pe server, login-ul nu va merge dacă nu autorizezi noul domeniu în Auth0.

1.  Intră pe [manage.auth0.com](https://manage.auth0.com).
2.  Mergi la **Applications** -> **Applications** -> Selectează aplicația ta (ThinkUp).
3.  În tab-ul **Settings**, caută secțiunile de URL-uri și adaugă domeniul tău (separat prin virgulă de localhost):
    *   **Allowed Callback URLs:** `https://domeniul-tau.ro/api/auth/callback`
    *   **Allowed Logout URLs:** `https://domeniul-tau.ro`
    *   **Allowed Web Origins:** `https://domeniul-tau.ro`
4.  Apasă **Save Changes** (jos de tot).

---

## ✅ Rezumat
1.  Ai luat VPS și Domeniu.
2.  Ai instalat Docker + codul.
3.  Ai configurat `.env` cu `AUTH0_BASE_URL=https://...`
4.  Ai importat datele (JSON).
5.  Ai pornit Tunnel-ul Cloudflare.
6.  Ai adăugat domeniul în dashboard-ul Auth0.

Gata! Site-ul e live.

