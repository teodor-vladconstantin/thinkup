import json
import logging
import urllib.request

from flask import request, abort
from .jwt_validator import Auth0JWTBearerTokenValidator
from insertoknameAuthlibFork.integrations.flask_oauth2 import ResourceProtector, current_token

require_auth = ResourceProtector()
AUTH0_DOMAIN = "dev-2ex6kfwedwudpdul.eu.auth0.com"

validator = Auth0JWTBearerTokenValidator(
    AUTH0_DOMAIN,
    "https://thinkup-api"
)
require_auth.register_token_validator(validator)


def current_user_id():
    """Derive this app's internal user id from the validated token's sub claim.

    Auth0 sub claims look like "google-oauth2|<id>" - this app's Users table
    and the frontend (useMyUser.js) both key on the part after the first "|".
    """
    sub = current_token.sub
    return sub.split('|', 1)[1] if '|' in sub else sub


def is_mentor(user_id=None):
    """True if user_id (default: the caller) is a Mentor in the Users table."""
    from dynamoDB import setup
    user = setup.startSetup('Users').getUser(user_id or current_user_id())
    return user.get('role') == 'Mentor'


def require_mentor():
    """Abort 403 unless the caller is a mentor. Call inside a @require_auth() route."""
    if not is_mentor():
        abort(403, description="Only mentors can do this")


def current_user_email():
    """Verified email of the caller, from Auth0 /userinfo (the request body can't be trusted).

    Returns None if Auth0 doesn't confirm a verified email.
    """
    try:
        req = urllib.request.Request(
            f"https://{AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": request.headers.get("Authorization", "")},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            info = json.load(resp)
    except Exception:
        logging.exception("Auth0 /userinfo lookup failed")
        return None
    return info.get("email") if info.get("email_verified") else None
