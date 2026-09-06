# SECURITY TODO — identitate reală a userului la apelurile API

**Status: problema rădăcină REZOLVATĂ — 2026-09-05, commit-uri `97eac49` (fix principal) + `4ec97d6` (documentație); configurare refresh token/`offline_access` (env + Auth0 dashboard, fără commit de cod separat).** `/api/token.js` emite acum tokenul real al userului logat (nu M2M), cu reînnoire silențioasă funcțională (refresh token, fără relogare la expirare), backend-ul acceptă și validează corect acest token, `current_token.sub` identifică userul real. Detalii complete în secțiunea "Rezolvat" de mai jos.

**Falsificabilitate prin body — REZOLVATĂ COMPLET, 2026-09-05, commit-uri `b73e44b` / `aefa9d0` / `f7ae03a` / `e4e521e`.** Toate rutele care citeau identitatea (`mentorId`/`created_by`) din body au fost migrate să folosească `current_token.sub`. Detalii complete în secțiunea "Rezolvat — falsificabilitate prin body" de mai jos.

**Reviews / Mentor Feedback / Personal Objectives — auth minim + ownership REZOLVATE, 2026-09-06, commit-uri `8f7a862` / `19f22a6` / `ab6d454`. Awards (cod mort) ȘTERS, commit `d66cbf8`. Bug Mentor.__init__ VERIFICAT funcțional (fără fix necesar).** Detalii complete în secțiunea "Rezolvat — auth + ownership pe Reviews/Mentor Feedback/Personal Objectives" de mai jos. OpenSchool rămâne intenționat doar cu autentificare (fără model de ownership în date — vezi aceeași secțiune).

## Problema

`platform-frontend/src/pages/api/token.js` emite tokenul Bearer folosit de `apiClient` (deci de toate cererile "autenticate" din aplicație) printr-un grant OAuth2 **client-credentials** (mașină-la-mașină):

```js
// pages/api/token.js
const response = await axios.post(`${issuerBaseUrl}/oauth/token`, {
  client_id: process.env.AUTH0_CLIENT_ID,
  client_secret: process.env.AUTH0_CLIENT_SECRET,
  audience: process.env.AUTH0_AUDIENCE,
  grant_type: "client_credentials"
});
```

Această rută **nu verifică deloc dacă cel care o apelează e logat** — e un endpoint Next.js public, needeclarat, needeclarat de sesiunea Auth0 a userului. Oricine poate face `GET /api/token` direct (fără cont, fără login) și primește un token Bearer valid, acceptat de toate rutele `@require_auth()` din backend.

Consecința: tokenul rezultat identifică **aplicația M2M**, nu userul care apasă butonul din browser. Claim-ul `sub` din acest JWT e constant — același pentru absolut toată lumea, indiferent cine e logat sau dacă e cineva logat. Backend-ul (`insertoknameAuthlibFork`'s `current_token`) n-are, structural, cum să afle cine anume face o cerere.

## Ce ar trebui făcut

Rutele care au nevoie de identitate reală a userului (nu doar "cineva cu token valid") ar trebui să valideze **sesiunea Auth0 a userului** (id_token / access_token per-user, obținut la login prin `@auth0/nextjs-auth0`), nu (doar) tokenul M2M al aplicației. Variante posibile, de discutat:

1. **Frontend trimite ambele tokenuri** — tokenul M2M pentru "acest request vine din aplicația noastră" + tokenul de sesiune al userului (sau id-ul lui, semnat/verificat server-side prin sesiunea Auth0 next.js) pentru identitate. Backend-ul verifică userul real din al doilea, nu-l mai "ghicește" din body.
2. **Backend validează sesiunea Auth0 direct** — rutele sensibile la identitate ar accepta tokenul de sesiune al userului (nu M2M), verificat cu `Auth0JWTBearerTokenValidator` deja existent în `utils/jwt_validator.py`, dar cu audience-ul potrivit unui token per-user, nu M2M.
3. Varianta minimă, dacă (1)/(2) sunt prea mult de schimbat acum: un endpoint intern (server-to-server, în Next.js API routes, care AU acces la sesiunea Auth0 a userului prin `@auth0/nextjs-auth0`) care semnează/atașează id-ul userului real la cerere înainte s-o trimită mai departe către Flask — mutând verificarea "cine e userul" în stratul Next.js (care chiar știe cine e logat), nu în Flask (care nu știe).

Oricare variantă aleasă, `/api/token` (sau echivalentul lui) ar trebui să refuze să emită un token dacă nu există o sesiune Auth0 validă în cererea originală a browserului.

## Rezolvat — 2026-09-05, commit `97eac49`

Varianta aleasă a fost cea mai simplă dintre cele trei discutate mai sus (nu a fost nevoie de nicio combinație): backend-ul nu avea, de fapt, nimic hardcodat pe M2M — `jwt_validator.py` verifică doar `exp`/`aud`/`iss`, indiferent de grant type. Login flow-ul (`pages/api/auth/[...auth0].js`) cerea deja audience-ul corect, moștenit automat din `AUTH0_AUDIENCE` în `.env.local` (verificat: `curl` pe `/api/auth/login` arăta deja `audience=https://thinkup-api` în redirect-ul spre Auth0, înainte de orice modificare). Singurul lucru care lipsea era ca `/api/token.js` să folosească acel token de sesiune în loc să ceară unul nou, M2M.

**Modificare:** `platform-frontend/src/pages/api/token.js` — `getAccessToken(req, res)` din `@auth0/nextjs-auth0` (v1.7.0, deja instalat) în loc de `axios.post(.../oauth/token, {grant_type: "client_credentials"})`. Fără sesiune → `401 {"error": "Not authenticated"}`, nu mai un token M2M ca fallback. `apiClient.js` — neschimbat comportamental (același shape de răspuns `access_token`/`expires_in`), doar comentariul actualizat.

**Testat pe producție, cu date reale, curățate/revertite după fiecare pas:**
- `GET /api/token` fără sesiune → `401`, confirmat că nu se mai scurge niciun token M2M către un caller nelogat.
- Login proaspăt (fereastră incognito, cont real) → `/api/token` a întors un JWT valid; decodat local (fără backend implicat): `sub: "google-oauth2|113528018155821801130"`, `aud` include `https://thinkup-api` — identitate reală, nu constanta M2M.
- Validatorul exact folosit de aplicație (`validator` din `utils/jwt_server.py`, importat și apelat direct, fără nicio rută de producție atinsă) a acceptat tokenul și a extras `sub` corect — confirmă că backend-ul, așa cum e azi, validează deja tokenuri de user, nu doar M2M.
- `PUT /projects/<id>/accept_reviews/0` → `1` (toggle + revert) și `PUT /projects/<id>` (editare nume/descriere prin multipart, ca în `EditProject.js`, + revert) cu tokenul real de user → `200` de fiecare dată, end-to-end prin HTTPS/nginx/Flask; aceleași rute fără token → `401`.

**Actualizare — 2026-09-05, aceeași zi:** limitarea de mai sus (fără refresh token, TTL fix 24h, relogare necesară) a fost rezolvată separat, în aceeași zi. Login-ul cere acum `offline_access` (`AUTH0_SCOPE` în `.env.local`, ambele medii), iar tenant-ul Auth0 are activat "Refresh Token" (grant type, pe aplicație) și — descoperit ca blocaj real în timpul testării, nu evident din start — **"Allow Offline Access" pe API-ul `ThinkUp API` însuși** (setare separată de grant-ul de pe aplicație; fără ea, Auth0 elimina tăcut `offline_access` din răspuns, fără eroare vizibilă). Testat pe producție cu login real, printr-o rută de diagnostic temporară (needeployed la git, ștearsă după test): sesiune nouă → `hasRefreshToken: true`; refresh forțat → token nou, cu `exp` mai târziu, `sub`/`aud` păstrate corect, fără eroare; `POST /projects/<id>` cu tokenul reînnoit → `200`, creat și șters curat. Nu există commit de cod pentru asta — doar `.env.local` (gitignored) și configurare Auth0 dashboard, ambele netrackuite în git.

## Rezolvat — falsificabilitate prin body, 2026-09-05

**Ce s-a rezolvat:** toate rutele care citeau identitatea (`mentorId`/`created_by`/`createdBy`) din body pentru decizia de autorizare au fost migrate să folosească `current_user_id()` (derivat din `current_token.sub`, funcția nouă din `platform-backend/src/utils/jwt_server.py`). Body-ul nu mai are niciun efect asupra cine e considerat owner/mentor — id-ul real vine exclusiv din tokenul validat. Fiecare grup a fost testat pe producție cu date reale (succes pentru owner/mentor real, `403` pentru impersonare cu id fals în body, curățat după fiecare test) — vezi ledger-ul de sesiune pentru detaliile per-test.

- **Grup 1 — Submissions + Warnings** (commit `b73e44b`): `POST /submissions/<challengeId>/<studentId>` (grade), `POST /submissions/project/...` (gradeProject), `POST /warnings/<studentId>` — `mentorId` din body → `current_user_id()`. Frontend (`grade.js`) nu mai trimite `mentorId` în payload.
- **Grup 2 — Projects PUT/DELETE** (commit `aefa9d0`): `created_by` din body → `current_user_id()`. Frontend (`EditProject.js`, `Settings/index.js`) nu mai trimite `created_by`.
- **Grup 3 — Challenges PUT/DELETE** (commit `f7ae03a`): `created_by` din body → `current_user_id()`, consolidat cu `_require_mentor()`. Frontend (`Challenges/index.js`) nu mai trimite `created_by`.
- **Grup 4 — Goals/Materials/Files** (commit `e4e521e`): `postGoal`/`updateGoal`/`deleteGoal`, `addMaterial`/`updateMaterial`/`deleteMaterial`, `postFile`/`deleteFile` — toate migrate la `current_user_id()`. `addMaterial` scrie acum și `createdBy` real în DB (înainte doar verifica, nu stoca corect). Frontend (`NewGoalPopUp.js`, `GoalPopUp.js`, `NewMaterialPopUp.js`, `MaterialCard.js`) nu mai trimite id-ul userului în payload; `Files` nu are niciun caller frontend, deci nimic de curățat acolo.

**Ce a rămas intenționat neatins (nu era în scope, nu falsificabilitate — routes de creare, nu de autorizare pe resursă existentă):** `POST /projects` (addProject) și `POST /challenges` (addChallenge) — creatorul e chiar userul care face requestul, nu există "altcineva" de impersonat la creare.

**Ce rămâne deschis, ca item SEPARAT:** rutele fără nicio verificare de identitate/rol (nu falsificabilitate — lipsă totală de control), listate mai jos.

## Rezolvat — auth + ownership pe Reviews/Mentor Feedback/Personal Objectives, 2026-09-06

**Ce s-a rezolvat:** cele 4 resurse care aveau doar `@require_auth()` (sau, pentru OpenSchool, nici măcar atât la un moment dat) au primit fiecare tratamentul potrivit structurii lor de date, verificat individual, nu presupus:

- **Reviews** (commit `8f7a862`) — ownership pe **autorul review-ului** (`userID`, cine a scris recenzia, nu owner-ul proiectului recenzat — verificat explicit în model înainte de implementare). `postReview` folosește `current_user_id()` în loc de `userID` din body (inclusiv pentru verificarea de "ai recenzat deja"); `updateReview`/`deleteReview` verifică review-ul existent față de `current_token.sub` → `403` dacă nu ești autorul. Fix găsit și reparat pe parcurs: `updateReview` (view) nu seta niciodată `id` din URL în body înainte de a-l trimite la DB layer, deci orice `PUT` crăpa cu `500 KeyError: 'id'` — bug preexistent, ruta nu avusese niciodată vreun apelant frontend real. Frontend (`AddReviewPopUp.js`) nu mai trimite `userID`.
- **Mentor Feedback** (commit `19f22a6`) — `addFeedback` verifică rolul (`Mentor`) din Users table pe baza `current_user_id()`, la fel ca la Submissions/Warnings, și folosește acel id ca `mentor_id` (nu cel din body). `editFeedack`/`deleteFeedback` verifică feedback-ul existent (`mentor_id`) față de `current_token.sub` → `403` dacă nu ești autorul. Frontend (`NewFeedbackPopUp.js`, `EditFeedbackPopUp.js`) nu mai trimite `mentor_id`.
- **Personal Objectives** (commit `ab6d454`) — ownership pe `userId` (elevul căruia îi aparțin). `postObjective` folosește `current_user_id()` în loc de `userId` din body; `updateObjective`/`deleteObjective` verifică obiectivul existent față de `current_token.sub` → `403` dacă nu ești owner-ul. Nu exista niciun apelant frontend pentru rută, deci nimic de migrat acolo. Două bug-uri preexistente găsite și reparate pe parcurs (blocau orice apel real către rută, niciodată executată până acum): `addPersonalObjective` apela `updateUser()` cu 3 argumente în loc de 4 (`coverPic` lipsă); `updateObjective` (view) nu avea `return`, deci `PUT`-ul reușea în DB dar tot răspundea cu `500`.
- **OpenSchool** — investigat explicit modelul de date (`IdOpenSchoolEncoder`/`OPEN_SCHOOL`): fișierele din OpenSchool **nu au niciun câmp de owner/creator** — e o bibliotecă comună, nu resurse per-user. Nu există relație de ownership de verificat. Rămâne intenționat doar cu `@require_auth()` (deja prezent) — barieră corectă și finală, nu un gap.
- **Awards** — ȘTERS complet (commit `d66cbf8`): `view_awards.py`, `api_crud_awards.py`, `db_crud_awards.py`, `award_encoder.py` erau cod mort — blueprint-ul `urlAwards` nu era înregistrat niciodată în `main.py`, iar `AwardsCard.js` din frontend e o componentă pur cosmetică cu props hardcodate, fără niciun fetch către backend (confirmat prin grep pe tot repo-ul). `model/entity/awards/awards.py` și `award.py` au fost păstrate — sunt încă importate (ca type hint) de `Student`/`Mentor`, deși folosite doar decorativ (userul se construiește cu `awards=[]`, o listă goală, nu o instanță `Awards`).
- **Bug `Mentor.__init__` (Faza 2)** — VERIFICAT cu test real pe producție, nu presupus: cont nou creat prin `POST /users` cu email pe domeniul `mentor.think-up.academy` → `200`, `role: "Mentor"` salvat corect în DB (verificat și control opus: email non-mentor → `role: "Student"`). Fix-ul din Faza 2 chiar funcționează; nimic de reparat.

**Testat pe producție cu date reale pentru toate cele 3 resurse cu ownership (Reviews, Mentor Feedback, Personal Objectives):** fără token → `401`; owner/mentor real → `200`, cu id-ul real stocat chiar și când body-ul conținea un id falsificat; non-owner (resursă seedată direct în DB cu alt id, sau — pentru rolul de Mentor — rol flipat temporar pe contul real al lui Duku și revertit imediat) → `403`. Toate datele de test șterse, orice listă/agregat atins (proiect, user) confirmat revenit la starea inițială.

## Ce rămâne — autentificare "oricine cu token" (fără verificare de identitate/rol deloc)
Rutele rămase fără verificare suplimentară de owner/rol — Goals POST (parte fără owner check unde nu era clar), Materials move up/down, Files GET, Users (toate rutele de scriere din `view_users.py`) — pentru toate astea, "identitatea reală" ar permite trecerea de la "orice user autentificat poate" la "doar userul potrivit poate", acolo unde are sens. Neschimbat, în afara scope-ului migrărilor de mai sus.

## Ce NU rezolvă acest fix, dar merită menționat separat

### Rezolvate — 2026-09-04, commit `8077d88`
Bug-uri funcționale găsite pe parcurs, nelegate de autorizare, reparate și testate cu date reale pe producție (curățate după):
- `db_crud_reviews.py::updateReview` — trei typo-uri boto3, nu unul: `ExpressionAttributes` → `ExpressionAttributeValues`, `UpdateExpression` fără virgule între atribute și cu prefixe `:#` invalide (`"set #uid=:#u #rvd=:#d #rvr=:#r"` → `"set #uid = :u, #rvd = :d, #rvr = :r"`), `ReturnValue` → `ReturnValues`. Testat: review creat cu `review_description="before-fix"`/`rating=3`, actualizat prin `PUT /reviews/update/...` la `"after-fix"`/`5`, confirmat prin `GET /reviews/<id>` că valorile chiar s-au schimbat în DB (nu doar că requestul nu mai crapă).
- `api_crud_files.py::delete_file` — la actualizarea materialului părinte după ștergerea unui fișier, trimitea id-ul fișierului șters în loc de id-ul materialului (`updateMaterial(idOfTheFile, ...)` → `updateMaterial(fileJson['materialId'], ...)`); update-ul eșua silențios (`{"ErrorMessage": "Material does not exist!"}`, ignorat de caller) și lista `files` a materialului rămânea cu id-ul fișierului șters. Testat: material real cu 2 fișiere, șters unul prin `DELETE /files/<id>`, confirmat că `files` conține DOAR fișierul rămas (nu ambele, nu niciunul).
- `view_gmail_contact.py` — eșec silențios dacă `CONTACT_MAIL_PASSWORD` lipsește din `.env`. Acum: verificare explicită la import-ul modulului (log `ERROR` clar la pornirea aplicației dacă lipsește) ȘI la apelul rutei (`sendContactInfo` refuză cu `abort(500, "Contact form is misconfigured (missing SMTP credentials) - message was not sent")` + log, în loc să încerce `mailer.login(contact_mail, None)`). Testat izolat, într-un proces separat cu variabila ștearsă doar pentru acel test (fără să ating `.env`-ul real sau serviciul live — editarea directă a `.env` de producție a fost blocată de clasificatorul de securitate al Claude Code, corect): confirmat log-ul de la pornire + `500` cu mesajul explicit, în loc de eșec tăcut.

### Găsite în timpul testării de mai sus

- **Parola Gmail din `.env` e respinsă de Google** (NEREZOLVAT, necesită acțiune din partea userului): `SMTPAuthenticationError: (535, 'Username and Password not accepted' ...)` la un test real de trimitere prin `/contact` cu variabila prezentă. Nu e legat de fix-urile de mai sus — App Password-ul Gmail curent pare expirat/revocat. Formularul de contact e efectiv nefuncțional în producție până când cineva generează un App Password nou în contul Google (`calex2005cj@gmail.com`) și îl pune în `.env`. (Fix-ul din 2026-09-04 tot ajută: acum eroarea asta apare clar în log, cu traceback, nu ca "ok" fals.)
- ~~`API_CRUD_REVIEWS.addReview`/`deleteReview` crapă pe `total_reviews` stocat ca string~~ — **INFIRMAT, 2026-09-04**: verificare directă în DynamoDB arată `total_reviews`/`average_rating` ca `Decimal`, nu string, pe ambele proiecte reale din DB; retestat `POST /projects/<id>/addReview/<reviewId>` și `DELETE /reviews/delete/...` cu un userID real (nu unul inventat) — ambele au funcționat corect (`total_reviews` 0→1→0, fără crash). Eroarea 500 observată inițial venea din `updateActivity()` (`api_track_activity.py`), care aruncă `KeyError: 'activity'` când `userID`-ul din body nu corespunde niciunui user real — exact ce se întâmpla cu userID-urile inventate folosite în testul precedent. În flux normal userID-ul vine dintr-un cont autentificat real, deci acest caz nu apare în producție; nu e un bug de reparat. (Observație minoră, separată, nelegată: `deleteReview` scade `total_reviews` dar nu recalculează `average_rating`, care rămâne la valoarea veche după ce ultima recenzie e ștearsă — cosmetic, nu crapă nimic.)
- `api_crud_files.py::download_file` / `getDetails` cu id inexistent — mesajul de eroare întors e `{"ErrorMessage": "User Does not Exist"}` (copiat greșit dintr-o altă entitate), cosmetic, nu blocant.
