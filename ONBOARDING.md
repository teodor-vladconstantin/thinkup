# 🚀 Ghid de Onboarding - Echipa ThinkUp

Bine ai venit în echipa de dezvoltare! Acest ghid te va ajuta să îți configurezi mediul de lucru local folosind Docker și Git, astfel încât să poți rula platforma în 10 minute.

## 🛠️ 1. Ce trebuie să instalezi?

Înainte de a începe, asigură-te că ai următoarele programe instalate:

1.  **Docker Desktop** (Obligatoriu)
    *   [Descarcă de aici](https://www.docker.com/products/docker-desktop/)
    *   ⚠️ **Important:** După instalare, deschide aplicația și asigură-te că vezi bulina verde (Engine Running) în stânga-jos.
2.  **Git**
    *   [Descarcă de aici](https://git-scm.com/downloads)
3.  **VS Code** (Recomandat)
    *   [Descarcă de aici](https://code.visualstudio.com/)

---

## 📥 2. Cum descarci proiectul?

Deschide un terminal (PowerShell, CMD sau Terminal în VS Code) și rulează:

```bash
# 1. Clonează repository-ul
git clone https://github.com/teodor-vladconstantin/thinkup.git

# 2. Intră în folder
cd thinkup
```

---

## 🔑 3. Configurare Secrete (Auth0)

Din motive de securitate, cheile de acces nu sunt pe GitHub. Trebuie să le configurezi manual.

1.  Mergi în folderul `platform-frontend`.
2.  Găsește fișierul `.env.example`.
3.  Fă o copie a acestuia și numește-o `.env.local`.
4.  Cere-i lui **Teodor** (sau pe grupul echipei) valorile pentru:
    *   `AUTH0_CLIENT_ID`
    *   `AUTH0_CLIENT_SECRET`
    *   etc.
5.  Salvează fișierul.

---

## 🚢 4. Pornirea Aplicației

Nu trebuie să instalezi Python, Node.js sau baze de date manual. Docker se ocupă de tot.

```bash
# 1. Mergi în folderul backend (unde e configurația Docker)
cd platform-backend

# 2. Pornește totul (durează 5-10 min prima dată)
docker-compose up --build -d
```

### Cum accesezi platforma?
După ce comanda s-a terminat și containerele rulează:
*   **Web (Frontend):** [http://localhost:3000](http://localhost:3000)
*   **API (Backend):** [http://localhost](http://localhost)
*   **Baza de date:** Rulează pe portul `8000` (ScyllaDB).

### Comenzi utile Docker:
*   **Oprire:** `docker-compose down`
*   **Vezi log-uri (erori):** `docker-compose logs -f`
*   **Restart:** `docker-compose restart`

---

## 💾 5. Importarea Datelor (Populare Bază de Date)

Când pornești aplicația prima dată, baza de date este goală. Pentru a avea utilizatorii și proiectele demo:

1.  Asigură-te că aplicația rulează (ai făcut pasul 4).
2.  Deschide un terminal nou și rulează:

```bash
docker exec -it thinkup-app python scripts/load_db_from_json.py
```
*Dacă primești eroare că nu găsește fișierul, asigură-te că ai rulat `docker-compose up --build` pentru a include noile fișiere.*

---

## 🌳 6. Cum lucrăm cu Git? (Reguli)

Pentru a nu ne șterge munca unii altora, respectăm următorul flux:

1.  **NU lucra pe `main`!** Ramura `main` este doar pentru codul final funcțional.
2.  **Creează-ți propria ramură (Branch)** când începi un task:
    ```bash
    git checkout main       # Mergi pe main
    git pull                # Ia ultimele noutăți
    git checkout -b nume-task-ul-tau  # Creează ramură nouă (ex: frontend-login-page)
    ```
3.  **Salvează modificările:**
    ```bash
    git add .
    git commit -m "Mesaj scurt despre ce ai făcut"
    git push origin nume-task-ul-tau
    ```
4.  **Unește codul (Merge):**
    *   Intră pe GitHub.
    *   Fă un **Pull Request (PR)** de pe ramura ta către `main`.
    *   Un coleg va verifica și va aproba modificarea.

---

## ❓ 7. FAQ (Probleme Comune)

**Q: Îmi merge foarte greu PC-ul când pornesc Docker.**
A: Docker consumă mult RAM. Intră în setările Docker Desktop -> Resources și limitează memoria la 4GB.

**Q: Primesc eroare de port (Port is already allocated).**
A: Probabil ai altceva deschis pe portul 3000 sau 8000. Închide alte servere (ex: Skype, alte proiecte Node) sau dă restart la PC.

**Q: Nu văd datele (Proiecte, Useri).**
A: Rulează comanda de la pasul **5. Importarea Datelor**. Dacă tot nu apar, verifică log-urile cu `docker-compose logs -f`.
