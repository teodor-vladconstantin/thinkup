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
Bug-uri funcționale găsite pe parcurs, nelegate de autorizare, nereparate:
- `db_crud_reviews.py::updateReview` — typo în parametrii boto3 (`ExpressionAttributes` vs `ExpressionAttributeValues`) — crash 500 mereu.
- `api_crud_files.py::delete_file` — după ștergere, actualizarea listei `files` a materialului părinte primește id-ul greșit (id-ul fișierului în loc de id-ul materialului) — fișierul șters poate rămâne listat în material.
- `view_gmail_contact.py` — dacă `CONTACT_MAIL_PASSWORD`/`2` lipsesc din `.env`, trimiterea de email va eșua silențios cu `None` ca parolă SMTP (nu crapă la pornire, doar la primul apel real).
