from .jwt_validator import Auth0JWTBearerTokenValidator
from insertoknameAuthlibFork.integrations.flask_oauth2 import ResourceProtector, current_token

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-2ex6kfwedwudpdul.eu.auth0.com",
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
