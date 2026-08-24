from .jwt_validator import Auth0JWTBearerTokenValidator
from insertoknameAuthlibFork.integrations.flask_oauth2 import ResourceProtector

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-2ex6kfwedwudpdul.eu.auth0.com",
    "https://thinkup-api"
)
require_auth.register_token_validator(validator)