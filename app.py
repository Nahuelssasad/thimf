
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


# Configure application
app = Flask(__name__)

#Time now
#now = datetime.now()
date_now =  datetime.now().strftime("%A, %d de %B de %Y, %H:%M:%S")