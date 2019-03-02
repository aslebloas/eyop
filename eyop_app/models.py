#!/usr/bin/env python3
"""Module with models"""
from eyop_app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.name)
