@echo off
start "" "http://127.0.0.1:5000/"
set FLASK_APP = website.py
flask run