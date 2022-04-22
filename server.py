from django.shortcuts import redirect
from flask import Flask,render_template,request,session,redirect,url_for
import sqlite3

app = Flask(__name__) #constructing app object
app.secret_key = "fc37c877f8194c3b0eee5e671b402475"
books =[{'bid':111,'title':'Java Springboot framework','author':'S John'},{'bid':112,'title':'Maths for Data Science','author':'Edison'},{'bid':113,'title':'Deep Learning with Tensorflow','author':'David'}]

""" @app.route('/')
@app.route("/home")
def home():
    return render_template('home.html',tit="Book Info",booksKey = books)
 """

@app.route('/bookselect/<aut_name>')
def book_select(aut_name):
    blist=[]
    for book in books:
        if book['author']==aut_name:
            blist.append(book)
    return render_template('bookSelection.html',booklist= blist)




@app.route('/varTest/<name>')
def variableTest(name):
    if name=='Admin':
        return 'Hello Admin'
    

    return f'hello , Good Afternoon {name}'

@app.route('/datatypeTest/<num>')
def dataTest(num):
    number = int(num)  # convert to int data type
    return f'square is {number*number}'


def check_password(pwd,cpwd):
    if len(pwd)>=8 and pwd==cpwd:
        return True
    else:
        return False



@app.route("/register",methods =['GET','POST'])
def home_page():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        fullname = request.form['fullname'] # it is the value of the name attribute in html form
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['con_password']
        gender = request.form['gender']
        address =request.form['address']
        if check_password(password,cpassword):
            with connect() as conn:
                sql ="insert into user (fullname,email,address,password, gender) values (?,?,?,?,?)"
                conn.execute(sql,(fullname,email,address,password,gender))
                conn.commit()
            return render_template('register_success.html',message=f"{fullname} {email} {password} {gender} {address} added to table")
        else:
            return redirect(url_for("home_page"))



        

def connect():
    conn = sqlite3.connect('bookShop.db')
    conn.row_factory= sqlite3.Row
    return conn



if __name__ == "__main__":
    app.run(port='5243',debug=True)



