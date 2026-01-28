
import sqlite3
import os
from flask import Flask, flash, redirect, render_template, request, session,url_for,jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from cachelib.file import FileSystemCache
from helpers import login_required,allowed_file

# Configure application
app = Flask(__name__)

# Configure session to use filesystem

app.config["SESSION_TYPE"] = "cachelib"
app.config['SESSION_SERIALIZATION_FORMAT'] = 'json'
app.config["SESSION_PERMANENT"] = False #Deleted when the browser is closed
app.config["SESSION_CACHELIB"] = FileSystemCache(cache_dir="flask_session")  # Esta es la línea clave

#Configure Uploading files
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS_IMG = {'png','jpg', 'jpeg','gif', 'webp','bmp'}
ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm', 'mpeg', 'mpg', 'm4v', '3gp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
@login_required
def index():
    if not session['id'] :
        return redirect("/")
    posts = None
    with sqlite3.connect("thimf.db") as con :
        con.row_factory = sqlite3.Row
    
        
        posts = con.execute("SELECT img,title,description,username FROM publications WHERE username = ?",(session['username' ],)).fetchall()
   
    return render_template("index.html",posts =posts,ALLOWED_EXTENSIONS_IMG = ALLOWED_EXTENSIONS_IMG,allowed_file = allowed_file)

@app.route("/login",methods=["GET","POST"])
def login():
    
    # Forget any user_id
    #session.clear()

    error = None

    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #Ensure username was submitted
        if not request.form.get("username"):
            flash("Debe ingresar un nombre de usuario")
            return render_template("login.html",class_error='alert-warning')


        #Ensure password was submitted
        if not request.form.get("password"):
            flash("Debe ingresar una contraseña")
            return render_template("login.html",class_error='alert-warning')
        

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
                    return render_template("login.html",class_error='alert-warning')
                
                #remember user has logged in
                session['id'] = result['id']
                session['username'] = result['username']
                #Redirect to page where user want to go
                next_page = '/'
                if next_page:
                    return redirect(next_page)
                return redirect("/")
            else:
                flash("Tienes que registrarte")
                return render_template("login.html",class_error='alert-warning')

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
            return render_template('register.html',class_error='alert-warning')
        #Validation length username
        if len(username) < 3:
            flash('username must have 3 or more characters',class_error='alert-warning')
            return render_template('register.html',class_error='alert-warning')
        #validation password
        if not password:
            flash('Missing password','error')
            return render_template('register.html',class_error='alert-warning')
        if len(password) < 8 :
            flash('Password must have 8 or more characters')
            
            return render_template('register.html',class_error='alert-warning')

        #Validation confirmation
        if not confirmation :
            flash('Must confirm your password')
            
            return render_template('register.html',class_error='alert-warning')
        #Verification password is equal confirmation
        if confirmation != password :
            flash('Password is not equal to confirmation ','error')
            
            return render_template('register.html',class_error='alert-warning')
        #Verification users existed
        with sqlite3.connect('thimf.db') as con :
            db = con.cursor()
            existing_user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if existing_user :
                flash('Username already exists','error',class_error='alert-warning')
                
                return render_template('register.html')
            #insert a new user in database

            try:

                db.execute('INSERT INTO users(username,hash_password) VALUES (?,?)', (username, generate_password_hash(password)))
                flash('Account created sucessfully!!You can now log in','success')
                
                return render_template('register.html',class_error='alert-success')
            
            except Exception as e:
                flash('Error try create the account.Try again',)
                
                return render_template("register.html",class_error='alert-warning')


    #Get information of register
    return render_template("register.html")

@app.route("/posts", methods=["POST"])

def posts():


    #dates form
    title = request.form.get('title')
    description = request.form.get('description')
    multimedia_file = request.files.get('image')
    username =session['username']
    
    #post

    #Verifications
    if not title:
        title = "..."
    if not description :
        description = "..."
    #Verification of img or video
    if not multimedia_file or multimedia_file.filename == "":
        filename = None

    elif not allowed_file(multimedia_file.filename,ALLOWED_EXTENSIONS_IMG) and not allowed_file(multimedia_file.filename,ALLOWED_EXTENSIONS_VIDEO):
        filename =None

    else:
        filename = secure_filename(multimedia_file.filename)
        path =os.path.join(app.config['UPLOAD_FOLDER'],filename)
        multimedia_file.save(path)

    
    #Insert dates
    with sqlite3.connect("thimf.db") as con:
        
        con.row_factory = sqlite3.Row

        con.execute("INSERT INTO publications(username,title,datatime,img,description) VALUES (?,?,?,?,?)",(username,title,date_now,filename,description))
       
        
    
    return redirect("/")
        
@app.route("/deletePost",methods = ['POST'])
@login_required
def deletePost():
    #delete register
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        username = request.form.get('username')


        with sqlite3.connect('thimf.db') as con:
            con.row_factory = sqlite3.Row

            con.execute("DELETE FROM publications WHERE username = ? AND description  = ?  AND title = ? ",(username,description,title))

    return redirect("/")



@app.route("/search")
@login_required
def search():
    return render_template("search.html")


@app.route("/searchAjax")
def searchAjax():
    query = request.args.get('q','').lower()
    
    with sqlite3.connect('thimf.db') as db :
        db.row_factory = sqlite3.Row
        posts_rows = db.execute('SELECT username,title,description,img FROM publications WHERE title LIKE ? OR username  LIKE ?',('%'+query+'%','%'+query+'%')).fetchall()

    
    posts = []
    for row in posts_rows :


        if allowed_file(row['img'],ALLOWED_EXTENSIONS_IMG):
            media_type = 'image'
        elif allowed_file(row['img'],ALLOWED_EXTENSIONS_VIDEO):
            media_type = 'video'
        else:
            media_type = 'none'



        posts.append({

            'username' : row['username'],
            'title': row['title'],
            'description':row['description'],
            'img' :row['img'],
            'media_type':media_type
        })

    
    return jsonify(posts)

#Initialize server flask
if __name__ == "__main__":
    app.run(debug=True)