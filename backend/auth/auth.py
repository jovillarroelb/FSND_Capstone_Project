import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Personal Project Specific:
AUTH0_DOMAIN = "jovillarroelb.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "projectapp"

## AuthError Exception
"""
AuthError Exception
A standardized way to communicate auth failure modes
"""


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


"""
FUNCTIONS:
"""

# Auth Header:
def get_token_auth_header():
    """
    Description: It obtains the header for the token.
    """

    auth_hdr = request.headers.get("Authorization", None)

    # If there is no header returned
    if not auth_hdr:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    # Split the header into its sub-parts:
    # Using ".split()" separates the "Bearer" string from the actual token.
    parts = auth_hdr.split()

    # The header has the correct number of sub-elements (ie. for BEARER tokens there are 2 parts)
    if len(parts) == 2:
        if parts[0].lower() != "bearer":
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": 'Authorization type needs to be "BEARER"',
                },
                401,
            )

        token = parts[1]

        return token

    # The header doesn't have the correct number of sub-elements (just 1 sub-part or more than 2).
    else:
        if len(parts) == 1:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "There is no token in the header",
                },
                401,
            )
        if len(parts) > 2:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Authorization must satisfy BEARER token format",
                },
                401,
            )


# Check Permissions:
def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid",
                "description": "No permissions in JWT",
            },
            400,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "Permission not found",
            },
            401,
        )
    return True


# Verify JWT:
def verify_decode_jwt(token):
    # Get public key from Auth0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # CHeck if the Auth0 token have a key id
    if "kid" not in unverified_header:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization malformed",
            },
            401,
        )

    rsa_key = {}

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            # Validate the token using the rsa_key
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                # issuer="https://" + AUTH0_DOMAIN + "/",
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
            return payload

        except jwt.ExpiredSignatureError:

            raise AuthError(
                {
                    "code": "token_expired",
                    "description": "Token expired.",
                },
                401,
            )

        except jwt.JWTClaimsError:

            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer.",
                },
                401,
            )

        except Exception:

            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )

    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


"""
AUTHENTICATION FUNCTION CONSTRUCTOR:
"""


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
