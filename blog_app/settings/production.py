from .settings import *
DEBUG = False
ALLOWED_HOSTS = ['*']  # Update with your domain
SECRET_KEY = config('SECRET_KEY')
try:
    from decouple import config
except ImportError:
    pass

