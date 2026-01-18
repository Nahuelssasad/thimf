
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from cachelib.file import FileSystemCache
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem

app.config["SESSION_TYPE"] = "cachelib"
app.config['SESSION_SERIALIZATION_FORMAT'] = 'json'
app.config["SESSION_PERMANENT"] = False #Deleted when the browser is closed
app.config["SESSION_CACHELIB"] = FileSystemCache(cache_dir="flask_session")  # Esta es la línea clave

Session(app)

#Time now
#now = datetime.now()
date_now =  datetime.now().strftime("%A, %d de %B de %Y, %H:%M:%S")



"""      """
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""  #Actualizacion del contenido
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"  
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/")

def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    
    # Forget any user_id
    session.clear()

    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #Ensure username was submitted
        if not request.form.get("username"):
            flash("Debe ingresar un nombre de usuario")
            return render_template("login.html") 

        #Redirect user to home page
        return redirect("/publications")





    
    return render_template("login.html")




@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/publications")
@login_required
def publications():
    return render_template("publications.html")









#Initialize server flask
if __name__ == "__main__":
    app.run(debug=True)