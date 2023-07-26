from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={"apiKey": "AIzaSyBxcsInmYLOYAtCJHB0AGcsOhmKuF6AQRo",
  "authDomain": "project-f9e36.firebaseapp.com",
  "projectId": "project-f9e36",
  "storageBucket": "project-f9e36.appspot.com",
  "messagingSenderId": "357168181223",
  "appId": "1:357168181223:web:d81db44a409480127b5742",
  "databaseURL":"https://project-f9e36-default-rtdb.europe-west1.firebasedatabase.app/"}


firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def signin():
    error= ""
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('profile'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['uname']
        biog = request.form['bio']
        name = request.form['fullname']
        try:
           login_session['user']= auth.create_user_with_email_and_password(email,password)
           user={'user':username, "fullname":name, "password":password, "bio":biog, "email": email}
           UID= login_session['user']['localId']
           db.child('users').child(UID).set(user)
           return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    posts = db.child('Posts').get().val()
    return render_template("home.html", posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    error=""
    if request.method=='POST':
        time = request.form['time']
        date = request.form['date']
        title = request.form['title']
        desc = request.form['desc']
        img = request.form['img']
        try:
            posts = {'img':img,'title':title,'uid': login_session['user']['localId'],'time':time,'desc':desc, 'date':date}
            db.child('Posts').push(posts)
            return redirect(url_for('home'))
        except:
            error = "error"
    return render_template("create.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template("profile.html")



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)