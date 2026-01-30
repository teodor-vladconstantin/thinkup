from .jwt_validator import Auth0JWTBearerTokenValidator
from insertoknameAuthlibFork.integrations.flask_oauth2 import ResourceProtector

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-v37jjjci.us.auth0.com",
    "https://test-api/api"
)
require_auth.register_token_validator(validator)