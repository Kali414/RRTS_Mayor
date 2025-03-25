from flask import Flask,session
from flask_cors import CORS
# from redis import Redis

import os

app=Flask(__name__)

CORS(app, supports_credentials=True)


# Required for Flask session to work
app.config["SECRET_KEY"] = "your_secret_key"

# app.config["SESSION_TYPE"] = "filesystem"
# app.config["SESSION_COOKIE_NAME"] = "session_id"
# app.config["SESSION_COOKIE_HTTPONLY"] = True
# app.config["SESSION_COOKIE_SECURE"] = False  # Set True in production with HTTPS
# app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Allow cross-site cookies
# Session(app)

# app.config["SESSION_TYPE"] = "redis"
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_USE_SIGNER"] = True
# app.config["SESSION_KEY_PREFIX"] = "flask_session:"
# app.config["SESSION_REDIS"] = redis.StrictRedis(host="localhost", port=6379, db=0)
# Session(app)

from app import routes