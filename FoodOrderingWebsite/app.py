
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
    dbCursor.execute("select food_id,food_name,food_price from FOOD")
    Food_details=dbCursor.fetchall()
    if request.method=='POST':
        food_id=request.form['food_id']
        name=request.form['name']
        price=request.form['price']
        food_image=request.files['food_image']
        food_image.save(os.path.join(os.getcwd()+'\static',secure_filename(food_id+'.jpg')))
        sql=("INSERT INTO FOOD (food_id,food_name,food_price) values(%s,%s,%s) ")
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

@app.route("/add_order",methods=['GET', 'POST'])
def add_order():
    dbCursor.execute("SELECT * FROM FOOD")
    food_list = dbCursor.fetchall()

    if request.method == "POST":

        # Retrieving food id and their counts from the cart
        food_count_dict = {}
        print(request.form)
        for item in request.form.getlist('card'):
            food_count_dict[int(item.split('-')[0].replace('card_',''))]=int(item.split('-')[1])

        # Retrieving customer id
        print('-----------------------------------------------------')

        customer_name = request.form.getlist('cust')[0]
        print(customer_name)
        dbCursor.execute(f"select * from customer where customer_name = '{customer_name}'")


        if len(dbCursor.fetchall()) == 0:
            dbCursor.execute(f"insert into customer (customer_name) values ('{customer_name}')")
            db.commit()

        dbCursor.execute(f"select * from customer where customer_name = '{customer_name}'")

        customer_id = dbCursor.fetchall()[0][0]
        print(customer_id)
        # Retrieving biggest order_id
        try:
            dbCursor.execute(f"select max(order_id) from customer_order")
            order_id = dbCursor.fetchall()[0][0] + 1
        except:
            order_id = 1

        # Inserting order in table
        for food_id,count in food_count_dict.items():
            
            dbCursor.execute(f"insert into customer_order values ({order_id},{customer_id},{food_id},{count},false)")

        db.commit()
        return redirect('/')
    return render_template("add_order.html",food_list=food_list)



@app.route("/display_order",methods=['GET', 'POST'])
def display_order():
    
    dbCursor.execute("select order_id,customer_name,food_name,status from ((customer_order INNER JOIN customer ON customer_order.customer_id = customer.customer_id) INNER JOIN food ON customer_order.food_id = food.food_id) where status = 0")
    order=dbCursor.fetchall()    
    print(order)
    
    return render_template('Displayf.html',title="All ordered food items",order=order)

@app.route("/update_status/<int:id>")
def update_status(id):
    dbCursor.execute("select order_id,customer_name,food_name,status from ((customer_order INNER JOIN customer ON customer_order.customer_id = customer.customer_id) INNER JOIN food ON customer_order.food_id = food.food_id) where status = 0")
    order=dbCursor.fetchall()
    l1=[]

    for i in order:
        if i[0]==id:
            l1.append((i[0],i[1],i[2],1))
            dbCursor.execute(f"update customer_order set status=1 where order_id={id}")
            db.commit()
        else:
            l1.append((i[0],i[1],i[2],0))
    return render_template('Displayf.html',title="All ordered food items",order=l1)

    
if __name__=="__main__":

    app.run(debug=True)