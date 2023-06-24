from flask import Flask,flash,redirect,url_for,request,render_template,flash,session
import mysql.connector
from flask_session import Session
from tkinter import *


app=Flask(__name__) 
'''
from key import secret_key,salt
from itsdangerous import URLSafeTimedSerializer
from stoken import token
from cmail import sendmail
import os

app.secret_key=secret_key
app.config['SESSION_TYPE']='filesystem'

user = os.environment.get('RDS_USERNAME')
host = os.environment.get('RDS_HOSTNAME')
db = os.environment.get('RDS_DB_NAME')
port = os.environment.get('RDS_PORT')
password = os.environment.get('RDS_PASSWORD')
with mysql.connector.connect(host=host,user=user,password=password,db=db) as conn:
    cursor=conn.cursor(buffered=True)
    cursor.execute("create table if not exists(username varchar(50) primary key,password varchar(15),email varchar(60))")
    cursor.execute("create table if not exists(nid int not null auto_increment primary key,title tinytext,content text,date timestamp default now() on update now(),added_by varchar(50),foreign key(added_by) references users(name))")
    cursor.close()
mydb=mysql.connector.connect(host=host,user=user,password=password,db=db)'''
mydb=mysql.connector.connect(host="localhost",user="root",password="mysql",db="survey")
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT count(*) from users where name=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['user']=username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/homepage')
def home():
    if session.get('user'):
        return render_template('homepage.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        password=request.form['password1']
        email=request.form['email']
        mobile=request.form['mobile']
        hotelname=request.form['hotelname']
        hotel_id=request.form['hotel_id']
        hoteladdress=request.form['hoteladdress']
        pin=request.form['pin']
        cursor=mydb.cursor(buffered=True)
        try:
            cursor.execute("insert into admins values(%s,%s,%s,%d,%s,%s,%d,%s)",(name,username,password,mobile,hotelname,hoteladdress,pin,email))
        except mysql.connector.IntegrityError:
            return 'username or email are already in use'
        else:
            mydb.commit()
            cursor.close()
            return redirect(url_for('login'))
    return render_template('signup.html')




app.run(use_reloader=True,debug=True)