import json
import logging
import time
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from joserfc.jwk import KeySet

JWKS_REFRESH_INTERVAL = 300  # seconds between refetches when a token fails to verify


class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        self.issuer = f"https://{domain}/"
        self._keys_loaded_at = 0
        super().__init__(self._fetch_jwks())
        self._keys_loaded_at = time.time()
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": self.issuer},
        }

    def _fetch_jwks(self):
        with urlopen(f"{self.issuer}.well-known/jwks.json", timeout=10) as resp:
            return KeySet.import_key_set(json.loads(resp.read()))

    def authenticate_token(self, token_string):
        claims = super().authenticate_token(token_string)
        # Auth0 may have rotated its signing keys - refetch them (rate-limited) and retry once
        if claims is None and time.time() - self._keys_loaded_at > JWKS_REFRESH_INTERVAL:
            try:
                self.public_key = self._fetch_jwks()
                self._keys_loaded_at = time.time()
            except Exception:
                logging.exception("JWKS refresh failed")
                return None
            claims = super().authenticate_token(token_string)
        return claims
