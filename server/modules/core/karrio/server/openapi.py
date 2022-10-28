from drf_spectacular.types import *
from drf_spectacular.utils import *
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class JWTAuthentication(OpenApiAuthenticationExtension):
    target_class = 'karrio.server.core.authentication.JWTAuthentication'
    name = 'JWT'

    def get_security_definition(self, auto_schema):
        return {
            'in': 'header',
            'type': 'apiKey',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'name': 'Authorization',
            "description": "Authorization: Bearer xxx.xxx.xxx",
        }


class TokenAuthentication(OpenApiAuthenticationExtension):
    target_class = 'karrio.server.core.authentication.TokenAuthentication'
    name = 'Token'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            "description": "Authorization: Token key_xxxxxxxx",
        }


class TokenBasicAuthentication(OpenApiAuthenticationExtension):
    target_class = 'karrio.server.core.authentication.TokenBasicAuthentication'
    name = 'TokenBasic'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'basic',
            'name': 'Authorization',
            "description": "-u key_xxxxxxxx:",
        }


class OAuth2Authentication(OpenApiAuthenticationExtension):
    target_class = 'karrio.server.core.authentication.OAuth2Authentication'
    name = 'OAuth2'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Authorization: Bearer xxxxxxxx",
        }
