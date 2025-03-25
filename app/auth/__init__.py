from flask import Flask, Blueprint

auth=Blueprint('auth',__name__)

from app.auth import routes