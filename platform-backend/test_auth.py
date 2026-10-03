"""Offline check of JWT validation. Run: PYTHONPATH=src python test_auth.py"""
import time

import flask
from joserfc import jwt
from joserfc.jwk import KeySet, RSAKey

from utils import jwt_validator

KEY = RSAKey.generate_key(2048, parameters={"kid": "k1"})
OTHER = RSAKey.generate_key(2048, parameters={"kid": "k2"})
jwks = {"keys": [KEY.as_dict(private=False)]}
jwt_validator.Auth0JWTBearerTokenValidator._fetch_jwks = lambda self: KeySet.import_key_set(jwks)

from utils.jwt_server import require_auth, current_user_id, AUTH0_DOMAIN, validator  # noqa: E402

app = flask.Flask(__name__)


@app.route("/me")
@require_auth()
def me():
    return current_user_id()


def token(key=KEY, **over):
    claims = {"sub": "google-oauth2|123", "iss": f"https://{AUTH0_DOMAIN}/",
              "aud": ["https://thinkup-api", f"https://{AUTH0_DOMAIN}/userinfo"],
              "exp": int(time.time()) + 600, **over}
    return jwt.encode({"alg": "RS256", "kid": key.kid}, claims, key)


def call(tok):
    return app.test_client().get("/me", headers={"Authorization": f"Bearer {tok}"} if tok else {})


r = call(token())
assert r.status_code == 200 and r.text == "123", (r.status_code, r.text)
assert call(None).status_code == 401
assert call(token(aud="https://other-api")).status_code == 401
assert call(token(exp=int(time.time()) - 3600)).status_code == 401
assert call(token(iss="https://evil.example/")).status_code == 401
assert call(token(key=OTHER)).status_code == 401

# Key rotation: once the refresh interval passed, a token signed with the new key is accepted
jwks["keys"].append(OTHER.as_dict(private=False))
validator._keys_loaded_at = 0
assert call(token(key=OTHER)).status_code == 200
print("ok")
