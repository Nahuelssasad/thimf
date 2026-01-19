
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session,url_for
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

    error = None

    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #Ensure username was submitted
        if not request.form.get("username"):
            flash("Debe ingresar un nombre de usuario")
            return redirect(url_for("login")) 


        #Ensure password was submitted
        if not request.form.get("password"):
            flash("Debe ingresar una contraseña")
            return redirect(url_for("login"))
        

        #Connect to db  
        with sqlite3.connect("thimf.db") as con:
            db = con.cursor()

            #Query database for username
            row = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()
          
        
           #Ensure username exists
            if row :
                result = dict(row) if hasattr(row, 'keys') else {'id': row[0], 'username': row[1], 'hash_password': row[2]}
            #check password
                if  not check_password_hash(result['hash_password'],request.form.get('password')):
                    flash("Contraseña incorrecta")
                    return render_template("login.html")
                
                #remember user has logged in
                session['id'] = result['id']
                #Redirect to page where user want to go
                next_page = request.form.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect("/")
            else:
                flash("Tienes que registrarte")
                return render_template("login.html")
            
     
            
            
            
    #User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")         
   
@app.route("/register",methods=["GET","POST"])
def register():
    """Register User"""

    #Clear session
    session.clear()

    if request.method ==  'POST':
        #Get data of form
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        #validation username
        if  not username :
            flash('Missing username','error')
            print(" missing username")
            return render_template('register.html')
        #Validation length username
        if len(username) < 3:
            flash('username must have 3 or more characters')
            print(" username length")
            return render_template('register.html')
        #validation password
        if not password:
            flash('Missing password','error')
            print(" missing password")
            return render_template('register.html')
        if len(password) < 8 :
            flash('Password must have 8 or more characters')
            print(" password length")
            return render_template('register.html')

        #Validation confirmation
        if not confirmation :
            flash('Must confirm your password')
            print(" missing confirmation")
            return render_template('register.html')
        #Verification password is equal confirmation
        if confirmation != password :
            flash('Password is not equal to confirmation ','error')
            print(" password not equal confirmation")
            return render_template('register.html')
        #Verification users existed
        with sqlite3.connect('thimf.db') as con :
            db = con.cursor()
            existing_user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if existing_user :
                flash('Username already exists','error')
                print(" existing user")
                return render_template('register.html')
            #insert a new user in database

            try:

                db.execute('INSERT INTO users(username,hash_password) VALUES (?,?)', (username, generate_password_hash(password)))
                flash('Account created sucessfully!!You can now log in','success')
                print(" user created")
                return redirect(url_for('login'))
            
            except Exception as e:
                flash('Error try create the account.Try again',)
                print(" error creating user")  
                return render_template("register.html")



    #Get information of register
    return render_template("register.html")

@app.route("/publications")
@login_required
def publications():
    return render_template("publications.html")

#Initialize server flask
if __name__ == "__main__":
    app.run(debug=True)