# Design: Proiecte legate de Challenge-uri reale

**Data:** 2026-09-05
**Status:** aprobat de user, gata pentru plan de implementare

## Context

Azi, un `Project` are un câmp liber `areaOfImplementation` (valorile hardcodate în frontend: "Civic Education", "Ecological", "STEM"), folosit doar ca etichetă/badge colorat, fără nicio legătură cu restul aplicației.

Separat, există deja un feature complet neutilizat: `Challenge` (id, name, description, deadline, maxScore, createdBy, creation_date) și `Submission` (notare mentor→elev pentru un challenge, cheie `challengeId#studentId`, doar scor+feedback, fără nicio legătură cu un proiect anume). Tabela `Challenges` e goală în producție; nu există nicio interfață frontend care să creeze/editeze challenge-uri sau să noteze un submission — doar `ScoreCard.js`/`DeadlineBanner.js`, care *citesc* submisii existente.

Cerința: categoria liberă a unui proiect e înlocuită cu o legătură reală către unul din 4 Challenge-uri, iar proiectul devine efectiv modul în care un elev participă la acel challenge (nu doar o etichetă cosmetică).

## Decizii confirmate cu userul

1. Proiectul DEVINE participarea la challenge (nu doar tag) — se unește cu fluxul de Submissions/notare existent.
2. Cele 4 Challenge-uri se creează printr-o pagină de admin nouă în frontend (nu doar seed direct în DB) — rutele backend CRUD deja există (`view_challenges.py`), doar frontend-ul lipsește.
3. Un elev poate avea EXACT UN proiect per challenge (nu mai multe) — impus la creare.
4. Când un proiect are mai mulți admini (echipă), la notare TOȚI adminii primesc aceeași notă/feedback (câte un `Submission` per admin).
5. Cele 2 proiecte reale existente (`mtega0tmtzvbkcudjoh`, `mtmntkh9asjptglks8`) sunt reasignate manual la Challenge 1 după ce acesta există în DB.

## Model de date

### `Project` (backend: `model/entity/project.py`, `model/entity/jsonencoders/project_encoder.py`)
- Elimină `areaOfImplementation` (`get_areOfImplementation`/`set_areOfImplementation`), adaugă `challengeId: str`.
- `ProjectEncoder.toJSON` scrie `challengeId` în loc de `areaOfImplementation`.
- `view_projects.py::addProject` — citește `challengeId` din body (în loc de `area_of_implementation`), și înainte de creare verifică: are userul (`created_by`) deja alt proiect cu același `challengeId`? Dacă da → `409` cu mesaj clar ("Ai deja un proiect pe acest challenge"). Verificarea se face iterând proiectele userului (`apiProjects.getOwnedProjects(created_by)`, deja existent) și comparând `challengeId`.
- `view_projects.py::updateProject` — la fel, acceptă `challengeId` în body-ul de update (înlocuiește orice referință la `areaOfImplementation`).

### `Submission` (backend: `model/entity/submission.py`, `model/entity/jsonencoders/submission_encoder.py`)
- Adaugă `projectId: str` (opțional la nivel de model, dar populat mereu de fluxul nou de notare).
- Cheia `id` rămâne `f"{challengeId}#{studentId}"` — neschimbată, păstrează semantica „un submission per elev per challenge" (consistent cu decizia #3).
- Rută nouă: `POST /submissions/project/<projectId>` (body: `mentorId`, `score`, `feedback` opțional) — citește proiectul, verifică `challengeId`-ul lui, iterează `adminList`, și creează/actualizează câte un `Submission` (`challengeId#adminId`) pentru fiecare admin, toate cu același `score`/`feedback`/`projectId`. Ruta veche `POST /submissions/<challenge_id>/<student_id>` rămâne neschimbată (nu e apelată de UI-ul nou, dar nimic n-o rupe).

## Piese de implementare (ordine de execuție)

### Piesa 1 — Legătura proiect↔challenge (fundația; se implementează prima, solo)
**Backend:** `Project`/`ProjectEncoder`/`view_projects.py` cum e descris mai sus.
**Frontend:**
- `NewProject/index.js`, `EditProject.js` — dropdown-ul citește `GET /challenges` (existent) în loc de array hardcodat `["Civic Education", "Ecological", "STEM"]`; trimite `challengeId` (nu `area_of_implementation`) la creare/update.
- `CategoryCard.js`/stilurile — afișează numele challenge-ului primit ca prop; culoarea badge-ului alocată pe poziția challenge-ului în lista de 4 (index 0-3 → una din 4 culori fixe definite în CSS), nu mai depinde de text hardcodat (`STEM`/`Ecological`/`Civic`).
- `ProjectsTable.js` — aceeași schimbare de sursă a categoriei (challenge în loc de areaOfImplementation).

**Migrare date:** după ce Challenge 1 există (cf. Piesa 2), reasignez direct în DB cele 2 proiecte reale la `challengeId` = id-ul lui Challenge 1.

**Testare pe producție:** creare proiect nou pe un challenge (200), a doua încercare pe același challenge pentru același user (409, mesaj clar), editare proiect schimbă challenge-ul (200), badge-ul afișează numele corect pe pagina proiectului. Curățenie: proiectele de test șterse la final.

### Piesa 2 — Pagină admin Challenges (independentă de Piesa 1, dar trebuie gata înaintea migrării datelor din Piesa 1)
**Frontend:** pagină nouă (CRUD: listă, creare, editare, ștergere), folosind rutele backend deja existente (`GET/POST/PUT/DELETE /challenges`). Acces ascuns în UI pentru non-mentori (verificare `user.role === 'Mentor'`, pattern deja folosit în aplicație).

**Backend (întărire necesară):** azi `POST/PUT/DELETE /challenges` au doar `@require_auth()`, fără nicio verificare de rol — oricine cu token poate crea/edita/șterge challenge-uri. Adaug verificare de rol Mentor pe aceste 3 rute, după același pattern deja folosit în `view_warnings.py`/`view_submissions.py` (id trimis în body, verificat față de `role` din tabela `Users`) — altfel pagina de admin ar fi doar o iluzie de restricție (oricine ar putea apela ruta direct).

**Testare pe producție:** creare Challenge 1-4 reale prin UI (200, verificat că apar în `GET /challenges`), editare unui challenge (200), ștergere unui challenge de test creat separat (200, curățat).

### Piesa 3 — Notare pe proiect (depinde de Piesa 1: are nevoie de `Project.challengeId` și `adminList`)
**Backend:** `view_submissions.py::gradeSubmission` + `Submission`/`SubmissionEncoder` cum e descris mai sus.
**Frontend:** pagină/UI nouă pentru mentori — listă de proiecte pe un challenge dat, cu formular de notare (scor + feedback opțional) per proiect, apelează noua rută de notare.

**Testare pe producție:** notare unui proiect real de test cu un singur admin (200, `Submission` creat cu `projectId` corect), notare unui proiect de test cu 2+ admini (200, câte un `Submission` identic per admin). Curățenie: submisiile și proiectele de test șterse la final.

### Piesa 4 — `DeadlineBanner`/`ScoreCard` (depinde de Piesa 1)
**Frontend:** `DeadlineBanner.js` — „nu am trimis încă" verifică acum dacă userul are un `Project` cu `challengeId` == challenge-ul respectiv (via `GET /user_projects/<id>`, deja existent), nu doar dacă există un `Submission`. `ScoreCard.js` rămâne pe logica de `Submission` pentru afișarea scorurilor (asta chiar reprezintă notarea, corect cum e azi).

**Testare pe producție:** user cu proiect pe un challenge cu deadline apropiat nu mai apare în banner ca "netrimis"; user fără proiect pe challenge apare corect.

## Ce NU e în scope acum
- Nu se construiește un flux de "depunere de lucrare" separat de proiect (fișiere/link atașate specific unui submission) — proiectul existent (cu goals/materials/photos) e considerat suficient ca "dovadă de lucru".
- Nu se schimbă `Submissions` pentru challenge-uri neasociate unui proiect (rutele vechi `GET /submissions/student/<id>` și `GET /submissions/challenge/<id>` rămân neschimbate).
- Nu se construiește o pagină publică de "browse projects by challenge" — doar dropdown-ul de selecție la creare/editare și badge-ul pe pagina proiectului.

## Execuție
Piesa 1 se implementează și se testează solo (fundația — celelalte au nevoie de contractul ei de date). După ce Piesa 1 e gata și testată pe producție, Piesele 2, 3, 4 se implementează în paralel prin subagenți independenți, fiecare cu un brief autonom bazat pe acest document (nume exacte de câmpuri/rute fixate în Piesa 1).
