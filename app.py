from flask import Flask, render_template, request, session
import os
from sqlalchemy.orm import sessionmaker
from database import *
from flask_bcrypt import Bcrypt

#CONNECTION WITH DB
engine = create_engine('sqlite:///intranet.db', echo=True)
app = Flask(__name__)
app.secret_key = os.urandom(64)
#PASSWORD ENCRYPTION
flask_bcrypt = Bcrypt(app)


@app.route('/')
def home():
    #IF YOU'RE NOT LOGGED IN SERVE LOGIN PAGE
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
    #ELSE REDIRECT TO DASHBOARD
        return dashboard()


@app.route('/dashboard')
def dashboard():


    #if you're not logged in you go back to login page
    if not session.get('logged_in'):
        return home()
    else:
        #create session
        Session = sessionmaker(bind=engine)
        s = Session()
        #get all data from db
        employees = s.query(EMPLOYEES).all()
        companies = s.query(COMPANIES).all()
        orders = s.query(ORDERS).all()
        #now we can print them at dashboard.html
        return render_template('dashboard/dashboard.html', employees=employees, companies=companies, orders=orders)





@app.route('/signup')
def signup():
    #checking if already logged in
    if not session.get('logged_in'):
        #serving registration page
        return render_template('signup.html')

    else:
        #if you're already logged in redirect to dashboard
        return dashboard()




@app.route('/register', methods=['POST'])
def register():
    # checking if already logged in
    if not session.get('logged_in'):
        #getting post data for registration
         POST_EMAIL = str(request.form['email'])
         POST_FNAME = str(request.form['fname'])
         POST_LNAME = str(request.form['lname'])
         POST_PHONE = int(request.form['phone'])
        #hashing password
         POST_PASSWORD = flask_bcrypt.generate_password_hash(str(request.form['password'])).decode('utf-8')
        #Creating session
         Session = sessionmaker(bind=engine)
         s = Session()
        #INSERTING DATA TO DB
         NEW_EMP = EMPLOYEES(POST_FNAME, POST_LNAME, POST_PHONE, POST_EMAIL, POST_PASSWORD)
         s.add(NEW_EMP)
         s.commit()
         return home()
    else:
        return dashboard()

@app.route('/createemp', methods=['POST'])
def createemp():
    #EMPLOYEE CREATION FROM DASHBOARD SAME WITH REGISTER ABOVE ^
    if session.get('logged_in'):
        #getting post data for registration
        POST_EMAIL = str(request.form['email'])
        POST_FNAME = str(request.form['fname'])
        POST_LNAME = str(request.form['lname'])
        POST_PHONE = int(request.form['phone'])
        #hashing password
        POST_PASSWORD = flask_bcrypt.generate_password_hash(str(request.form['password'])).decode('utf-8')

        #Putting data into DATABASE
        Session = sessionmaker(bind=engine)
        s = Session()

        NEW_EMP = EMPLOYEES(POST_FNAME, POST_LNAME, POST_PHONE, POST_EMAIL, POST_PASSWORD)
        s.add(NEW_EMP)
        s.commit()
        return dashboard()
    else:
        return home()

@app.route('/createorder', methods=['POST'])
def creatorder():
    #ORDER CREATION FROM DASHBOARD
    if session.get('logged_in'):
        #getting post data for order creation
        POST_CNAME = str(request.form['cname2'])
        PRODUCTS = str(request.form['products'])
        POST_DATEM = str(request.form['datem'])
        POST_DATED = str(request.form['dated'])


        #INSERTING data into DATABASE
        Session = sessionmaker(bind=engine)
        s = Session()

        NEW_ORD = ORDERS(POST_CNAME, PRODUCTS, POST_DATEM, POST_DATED)
        s.add(NEW_ORD)
        s.commit()
        return dashboard()
    else:
        return home()


@app.route('/createcomp', methods=['POST'])
def createcomp():
    if session.get('logged_in'):
        #COMPANY CREATION FROM DASHBOARD
        POST_CNAME = str(request.form['cname'])
        POST_DESCRIPTION = str(request.form['description'])


        #INSERTING data into DATABASE
        Session = sessionmaker(bind=engine)
        s = Session()

        NEW_COMP = COMPANIES(POST_CNAME, POST_DESCRIPTION)
        s.add(NEW_COMP)
        s.commit()
        return dashboard()
    else:
        return home()





@app.route('/login', methods=['POST'])
def login():
    #CHECKING IF YOU'RE ALREADY LOGGED IN
    if not session.get('logged_in'):
        #GETTING DATA FROM THE LOGIN FORM
        POST_EMAIL = str(request.form['email'])
        POST_PASSWORD = str(request.form['password'])
        #CREATING SESSION
        Session = sessionmaker(bind=engine)
        s = Session()
        #CREATING QUERY
        USR_LOGIN = s.query(EMPLOYEES).filter_by(EMAIL=POST_EMAIL).first()
        if USR_LOGIN:
            #CHECKING IF HASHED PASSWORD  MATCHES TO LOGIN PASSWORD
            if flask_bcrypt.check_password_hash(USR_LOGIN.PASSWORD, POST_PASSWORD):
                session['logged_in'] = True
                return home()
        else:
            return home()

    else:
        return home()


@app.route("/remove/<string:wow>", methods=['post'])
def remove(wow):
    # ROW REMOVAL FROM EMPLOYEES TABLE

    Session = sessionmaker(bind=engine)
    s = Session()
    employee = s.query(EMPLOYEES).filter_by(EMP_ID=wow).first()
    s.delete(employee)
    s.commit()
    return dashboard()





@app.route("/remove1/<string:wow>", methods=['post'])
def remove1(wow):
    # ROW REMOVAL FROM COMPANIES TABLE
    Session = sessionmaker(bind=engine)
    s = Session()
    COMPANY = s.query(COMPANIES).filter_by(COMPANY_NAME=wow).first()
    s.delete(COMPANY)
    s.commit()
    return dashboard()


@app.route("/remove2/<string:wow>", methods=['post'])
def remove2(wow):
    #ROW REMOVAL FROM ORDERS TABLE
    Session = sessionmaker(bind=engine)
    s = Session()
    ORDER = s.query(ORDERS).filter_by(ORDER_ID=wow).first()
    s.delete(ORDER)
    s.commit()
    return dashboard()

@app.route("/logout")
def logout():
    #logout
    session['logged_in'] = False
    return home()




if __name__ == "__main__":
    app.run(debug=True)

