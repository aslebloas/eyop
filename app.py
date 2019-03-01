#!/usr/bin/env python3
"""App routes"""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "index"


@app.route('/profile')
def profile():
    return "profile"


@app.route('/register')
def register():
    return "register"


@app.route('/login')
def login():
    return "login"


@app.route('/logout')
def logout():
    return "logout"
