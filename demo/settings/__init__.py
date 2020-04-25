import os

ENV_NAME = os.getenv('ENV_NAME', 'local')

if ENV_NAME == 'prod':
    from .production import *
elif ENV_NAME == 'develop':
    from .development import *
