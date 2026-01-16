
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from cachelib.file import FileSystemCache


# Configure application
app = Flask(__name__)

# Configure session to use filesystem

app.config["SESSION_TYPE"] = "cachelib"
app.config['SESSION_SERIALIZATION_FORMAT'] = 'json'
app.config["SESSION_PERMANENT"] = False #Deleted when the browser is closed

Session(app)

#Time now
#now = datetime.now()
date_now =  datetime.now().strftime("%A, %d de %B de %Y, %H:%M:%S")