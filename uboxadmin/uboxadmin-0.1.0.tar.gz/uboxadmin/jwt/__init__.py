from rest_framework_simplejwt import state

from .compat import token_backend

state.token_backend = token_backend
