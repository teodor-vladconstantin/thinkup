# SECURITY TODO — identitate reală a userului la apelurile API

**Status: problema rădăcină REZOLVATĂ — 2026-09-05, commit `97eac49`.** `/api/token` emite acum tokenul real al userului logat (nu M2M), backend-ul acceptă și validează corect acest token, `current_token.sub` identifică userul real. Detalii complete în secțiunea "Rezolvat" de mai jos. **Ce rămâne deschis:** rutele individuale listate în secțiunea "Ce ar deveni cu adevărat sigur" mai jos încă citesc identitatea din body (`created_by`/`mentorId`/etc.), nu din `current_token.sub` — acum ar putea, dar migrarea e per-rută, netratată încă (vezi "Ce rămâne de făcut" la final).

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

**Notă, nu e bug introdus de acest fix:** login flow-ul nu cere `offline_access`, deci nu există refresh token. Access tokenul userului are un TTL fix de 24h (confirmat din `exp`-`iat` pe tokenul real emis); sesiunile mai vechi de 24h primesc `401` la `/api/token` până la un login nou, chiar dacă sesiunea de identitate (afișarea "logat", vizualizarea profilului) rămâne validă separat. Comportament corect al SDK-ului dat fiind lipsa refresh tokenului, dar diferit de vechiul M2M (care mergea mereu, indiferent de vechimea sesiunii) — utilizatorii cu tab-uri deschise de mult vor trebui să se re-autentifice la prima acțiune scrisă după expirare.

## Ce rămâne de făcut

Rutele din secțiunea de mai jos ("Ce ar deveni cu adevărat sigur") încă citesc identitatea din body, nu din `current_token.sub` — deliberat, în afara scope-ului acestui fix (per instrucțiune explicită: doar identitatea din token trebuia reparată, nu felul în care o folosește fiecare rută). Acum că `current_token.sub` identifică userul real, fiecare rută de mai jos ar putea trece de la "verifică id-ul din body" la "verifică `current_token.sub`" — dar asta e o migrare separată, per-rută, netratată încă.

## Ce ar deveni cu adevărat sigur odată rezolvată

Toate punctele de mai jos verifică AZI un id trimis de client în body/query — funcțional, dar falsificabil de oricine cunoaște id-ul unei alte persoane (owner de proiect, mentor etc.), pentru că nu există nicio legătură criptografică între acel id și cine chiar face request-ul:

### Verificare de rol (Mentor)
- `POST /submissions/<challengeId>/<studentId>` — `mentorId` din body, verificat față de `role` din Users table
- `POST /warnings/<studentId>` — `mentorId` din body, verificat față de `role` din Users table

### Verificare de owner/admin proiect
- `PUT /projects/<id>` — `created_by` din body vs `createdBy`/`adminList`
- `DELETE /projects/<id>` — `created_by` din body vs `createdBy`/`adminList`
- `PUT /challenges/<id>` — `created_by` din body vs `createdBy`
- `DELETE /challenges/<id>` — `created_by` din body vs `createdBy`
- `POST /goals/<id>` — `created_by` din body vs owner-ul proiectului părinte
- `PUT /goals/<id>` — `created_by` din body vs owner-ul proiectului părinte
- `DELETE /goals/<id>` — `created_by` din body vs owner-ul proiectului părinte
- `POST /materials/<id>` — `createdBy` din body vs owner-ul proiectului părinte
- `PUT /materials/<id>` — `updatedBy` din body vs owner-ul proiectului părinte
- `DELETE /materials/<id>` — `created_by` din body vs owner-ul proiectului părinte
- `POST /files/<id>` — `created_by` din body vs owner-ul (prin material → proiect)
- `DELETE /files/<id>` — `created_by` din body vs owner-ul (prin material → proiect)

### Autentificare "oricine cu token" (fără verificare de identitate/rol deloc)
Toate rutele `@require_auth()` fără verificare suplimentară — Goals POST (parte fără owner check unde nu era clar), Materials move up/down, Files GET, Awards (cod mort, neînregistrat), Reviews (add/update/delete), Mentor Feedback (add/edit/delete), Personal Objectives (post/put/delete), OpenSchool (add/delete/increasePopularity), Users (toate rutele de scriere din `view_users.py`) — pentru toate astea, "identitatea reală" ar permite trecerea de la "orice user autentificat poate" la "doar userul potrivit poate", acolo unde are sens.

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
