
from logging import disable
import os
import flask_bcrypt
from flask import Flask,render_template,request,session,redirect,g,url_for
from werkzeug.utils import secure_filename
from forms import LoginForm,RegistrationForm,Adminloginform
from mysqldb import dbCursor,db
from flask_bcrypt import Bcrypt
from io import BytesIO


bcrypt = Bcrypt()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab0d2f821826296ce6ff45fa2febb555'


@app.before_request
def before_request():
    print(session)
    if 'user_id' in session:
        try:
            dbCursor.execute(f"SELECT * FROM USER where user_id = {session['user_id']}")
            record = dbCursor.fetchall()[0]
            print(record)
            g.user = record
            print(g)
        except:
            print("There was an error retrieving your previous login.")
            session.pop('user_id')


@app.route("/")
def home_page():
    return render_template('home.html')


@app.route("/login",methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        session.pop('user_id',None)
        print(f'SELECT * FROM USER where username = "{form.Username.data}"')
        dbCursor.execute(f'SELECT * FROM USER where username = "{form.Username.data}"')
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
       
        return redirect(url_for('login_page'))
    return render_template('register.html',title="Register Page", form=form)


@app.route("/admin",methods=['GET', 'POST'])
def log_admin():
    form=Adminloginform()
    if form.validate_on_submit:
        
        session.pop('user_id',None)
        print(f'SELECT * FROM ADMIN where username = "{form.username.data}"')
        dbCursor.execute(f'SELECT * FROM ADMIN where username = "{form.username.data}"')
        # record = dbCursor.fetchall()[0]
        
        return redirect('/userdb')
    return render_template('admin.html',title="Admin login Page",form=form)
        
# @app.route("/admin_see",methods=['GET','POST'])
# def admin_pg():
#     details=dbCursor.fetchall()[0]

@app.route("/userdb",methods=['GET', 'POST'])
def showdb():
    
    dbCursor.execute("select user_id,username,email from USER")
    details=dbCursor.fetchall()
    
    return render_template('admin_see.html',title="User Database",details=details)

@app.route("/addfooditems",methods=['GET','POST'])
def add_food():
    dbCursor.execute("select food_id,food_name,price from FOOD")
    Food_details=dbCursor.fetchall()
    location="C:\\Users\\GAJENDRA\\Desktop\\Food-Ordering-System\\FoodOrderingWebsite\\static"
    if request.method=='POST':
        food_id=request.form['food_id']
        name=request.form['name']
        price=request.form['price']
        food_image=request.files['food_image']
        food_image.save(os.path.join(location,secure_filename(food_image.filename)))
        sql=("INSERT INTO FOOD (food_id,food_name,price) values(%s,%s,%s) ")
        val=(food_id,name,price)
        dbCursor.execute(sql,val)
       
        db.commit()
        print(dbCursor.rowcount, "record inserted.")
        return redirect('/addfooditems')
    return render_template('addfooditems.html',title="Add Food items",Food_details=Food_details)




@app.route("/logout")
def logout_page():
    session.pop('user_id')
    g.pop('user')
    return redirect('/home')


