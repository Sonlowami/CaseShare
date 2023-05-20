#!/usr/bin/python3
"""
This file contains a python
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def index():
    return render_template('index.html')

@app.get('/login', strict_slashes=False)
def login():
    return render_template('login.html')

@app.get('/register', strict_slashes=False)
def register():
    return render_template('register.html')