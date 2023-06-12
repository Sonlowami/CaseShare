#!/usr/bin/python3
"""
This file contains a python
"""
from flask import Flask, render_template, redirect

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

@app.get('/logout', strict_slashes=False)
def logout():
    return render_template('logout.html')

@app.get('/features', strict_slashes=False)
def features():
    return render_template('features.html')

@app.get('/about_us', strict_slashes=False)
def about_us():
    return render_template('about_us.html')

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Accepts,Authorization,x-token,x-requested-with")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE")
    return response
