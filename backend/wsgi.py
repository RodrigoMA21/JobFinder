import os

os.environ.setdefault("APP_ENV", "production")
os.environ.setdefault("PYTHONANYWHERE", "1")

from a2wsgi import ASGIMiddleware
from app.main import app

application = ASGIMiddleware(app)
