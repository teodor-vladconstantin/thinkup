# SECURITY TODO — identitate reală a userului la apelurile API

**Status:** documentat, NEIMPLEMENTAT. Nu necesită fix urgent — toate rutele de scriere au acum minim o barieră de autentificare (token valid) și, unde există un concept de proprietate, o verificare de owner. Ce lipsește e legarea criptografică a acelei verificări de userul care chiar face cererea.

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
