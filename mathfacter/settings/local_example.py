from mathfacter.settings.dev import *

HOST_IP_ADDR = "localhost"

ALLOWED_HOSTS = [HOST_IP_ADDR]
CORS_ORIGIN_WHITELIST = [
    "http://{}:3000".format(HOST_IP_ADDR),
]
CORS_ALLOW_CREDENTIALS = True
