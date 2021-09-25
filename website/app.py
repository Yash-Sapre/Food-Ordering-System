from enum import unique
import flask_bcrypt
from flask import Flask,render_template,request,session,redirect,g,url_for
from forms import LoginForm,RegistrationForm
from mysqldb import dbCursor,db
from flask_bcrypt import Bcrypt
from flask_login import login_user,logout_user,current_user,LoginManager


bcrypt = Bcrypt()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab0d2f821826296ce6ff45fa2febb555'


@app.before_request
def before_request():
    if 'user_id' in session:
        record = dbCursor.execute(f"SELECT * FROM USER where user_id = {session['user_id']}")[0]
        g.user = record


@app.route("/home")
def home_page():
    return render_template('home.html',item={'Phone':8605517160})


@app.route("/login",methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        session.pop('user_id',None)
        dbCursor.execute(f'SELECT * FROM USER where email = {form.Email.data}')
        record = dbCursor.fetchall()[0]
        if record is not None:
            if bcrypt.check_password_hash(record[2],form.Password.data):
                session['user_id'] = record[0]

    return render_template('login.html',title="Login Page",form=form)


@app.route("/register",methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = flask_bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        print(f'{form.Username.data}')
        print(f'{hashed_password}')
        print(f"INSERT INTO USER (username,password,email) VALUES ('{form.Username.data}','{hashed_password}','{form.Email.data}')")
        dbCursor.execute(f"INSERT INTO USER (username,password,email) VALUES ('{form.Username.data}','{hashed_password}','{form.Email.data}')")
        db.commit()
        print('c')
        return redirect(url_for('login_page'))
    return render_template('register.html',title="Register Page",form=form)


@app.route("/logout")
def logout_page():
    session.pop['user_id']
    return redirect('/home')


