import os

from .client import Client
from .errors import Unauthorized, BadRequest, AuthenticationFailed


def with_token(token):
    client = Client(base_url(), docker_host())

    try:
        client.token = token
        client.bootstrap()
        return client
    except Unauthorized:
        raise AuthenticationFailed()


def with_username_and_password(username, password):
    client = Client(base_url(), docker_host())

    try:
        client.token = client.request("POST", "/signin", data={"username": username, "password": password}, quiet=True)["token"]
        client.bootstrap()
        return client
    except BadRequest:
        raise AuthenticationFailed()


def base_url():
    return os.environ.get('ORCHARD_API_URL', 'https://orchardup.com/api/v1')


def docker_host():
    return os.environ.get('ORCHARD_DOCKER_HOST', 'https://%s.orchardup.net')
