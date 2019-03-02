#!/usr/bin/env python3
"""App routes"""
from eyop_app import app
from flask import render_template


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    return "logout"

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
