
from flask import Flask,render_template,request,session,redirect,url_for,flash
import os
import sqlite3

app = Flask(__name__) #constructing app object
app.secret_key = "fc37c877f8194c3b0eee5e671b402475"
app.config['UPLOAD']="static/images"
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
@app.route('/home')
def userhome():
    return redirect(url_for('login'))


@app.route("/register",methods =['GET','POST'])
def home_page():
    if request.method == 'GET':
        return render_template('register.html')
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
                flash('Register success! Please login','success')
            return render_template('login.html')
        else:
            flash('Password length must be 8 characters or password and confirm password must be the same ','danger')
            return redirect(url_for("home_page"))

        

def connect():
    conn = sqlite3.connect('bookShop.db')
    conn.row_factory= sqlite3.Row
    return conn

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        form_password = request.form['password']
        with connect() as conn:
            cursor = conn.cursor()
            sql = "select password from user where email=?"
            row = cursor.execute(sql,(email,)).fetchone()
            
            
            if row is None:
                flash('username does not exist. Try again','warning')
                return redirect(url_for('login'))
            else:
                db_password = row[0]
                if db_password == form_password:
                    session['user']= email
                    flash('login success!!!','success')
                    return render_template('login_success.html')
                else:
                    flash('Password is wrong. Try again','warning')
                    return redirect(url_for('login'))

@app.route('/checkOut')
def checkOut():
    if 'cart' in session:
        if len(session['cart'])>0:
            cart = session['cart']
            basket={}
            for bid,qty in cart.items():
                basket[bid]=qty
            bookInfo={}
            with connect() as conn:
                cursor = conn.cursor()
                totalAmount = 0
                for k,v in basket.items():
                    amt=0
                    row = cursor.execute("select * from book where bid=?",(k)).fetchone()
                    amt = row[3]* int(v)
                    totalAmount += amt
                    bookInfo[k] =[row,v,amt]
            return render_template('checkout.html',bookInfo = bookInfo, tamt =totalAmount)
        else:
            return "there is no item in your cart"
                   




        return  render_template('checkout.html',bookInfo= bookInfo)
    else: return "there is no items in your cart"


@app.route('/purchase',methods=['POST'])
def purchase():
    if 'user' in session:
        bookid = request.form['bid']
        qty = request.form['qty']
        if 'cart' not in session:
            session['cart']=None
            cart={}
            cart[bookid] = qty
            session['cart']= cart
        else:
            cart = session['cart']
            if bookid in cart:
                oldqty = cart[bookid]
                cart[bookid]= oldqty + qty
            else:
                cart[bookid] = qty
            session['cart'] = cart
        return redirect(url_for('user_view_book'))
    else:
        return redirect(url_for('login'))






@app.route('/userViewBook')
def user_view_book():
    if 'user' in session:
        with connect() as conn:
            cursor = conn.cursor()
            sql = 'select * from book'
            row = cursor.execute(sql)
           
            
            return render_template('userViewBook.html',books = row)
    else:
        return redirect(url_for('login'))




@app.route('/logout')
def logout():
    session.clear()
    # redirect to a particular function name
    return redirect(url_for('login'))


""" The following part is for admin site"""
@app.route('/adminHome')
def admin_home():
    return render_template("adminhome.html")

@app.route('/bookInsert',methods=['GET',"POST"])
def book_insert():
    if request.method == 'GET':
        return render_template('book.html')
    else:
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        category = request.form['category']
        bookcover = request.files['bfile']
        filename = bookcover.filename  # retrieving filename from file object named bookcover
        bookcover.save(os.path.join(app.config['UPLOAD'],filename))
        description = request.form['description']
        with connect() as conn:
            sql ="insert into book (title,author,price,category,description,cover) values (?,?,?,?,?,?)"
            
            
            cursor = conn.cursor()
            cursor.execute(sql,(title,author,price,category,description,filename))
            if cursor.rowcount>0:
                return redirect(url_for('view_book'))
            else:
                flash("something wrong in sql syntax")

        return redirect(url_for('admin_home'))

@app.route('/viewBook')
def view_book():
    if 'admin' in session:
        with connect() as conn:
            cursor = conn.cursor()
            sql = 'select * from book'
            row = cursor.execute(sql)
            if row is None:
                return render_template('adminLogin_success.html')
            else:
                return render_template('viewBook.html',books = row)
    else:
        return redirect(url_for('admin_login'))


@app.route('/deleteBook',methods=['POST'])
def delete_book():
    if 'admin' in session:
        book_id = request.form['bid']
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("delete from book where bid=?",(book_id))
            if cursor.rowcount>0:
                flash('book has been deleted ','info')
                
            else:
                flash('something went wrong in deletion')
        return redirect(url_for('view_book'))
    else:
        redirect(url_for('admin_login'))







@app.route('/updateBook',methods=['GET','POST'])
def update_book():
    if 'admin' in session:
        if request.method == 'GET':
            with connect() as conn:
                cursor = conn.cursor()
                sql = 'select * from book'
                row = cursor.execute(sql)
                return render_template('editBook.html',books = row)

        else:
            return "in post"
    else:
        return redirect(url_for('admin_login'))


@app.route('/editBook2',methods=['POST'])
def edit_book():
    if 'admin' in session:
        bookid = request.form['bid']
        with connect() as conn:
            cursor = conn.cursor()
            sql = 'select * from book where bid=?'
            result_book = cursor.execute(sql,(bookid)).fetchone()
            return render_template('editBookForm.html',book = result_book)
    else:
        return redirect(url_for('admin_login'))


@app.route('/updateBook2', methods=['POST'])
def update_bookfinal():
    title = request.form['title']
    author = request.form['author']
    price = request.form['price']
    descr =request.form['description']
    book_id = request.form['bid']
    with connect() as conn:
        cursor = conn.cursor()
        sql ='update book set title=? , author=?, price=?,description =? where bid=?'
        cursor.execute(sql,(title,author,price,descr,book_id))
        if cursor.rowcount>0:
            return redirect(url_for('update_book'))
        else:
            flash('update fail','warning')
            return redirect(url_for('update_book'))



        





@app.route('/adminLogin',methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('adminLogin.html')
    else:
        email = request.form['email']
        form_password = request.form['password']
        with connect() as conn:
            cursor = conn.cursor()
            sql = "select password from admin where email=?"
            row = cursor.execute(sql,(email,)).fetchone()
            
            
            if row is None:
                flash('username does not exist. Try again','warning')
                return redirect(url_for('admin_login'))
            else:
                db_password = row[0]
                if db_password == form_password:
                    session['admin']= email
                    flash('login success!!!','success')
                    return render_template('adminSuccess.html')
                else:
                    flash('Password is wrong. Try again','warning')
                    return redirect(url_for('admin_login'))
                



@app.route('/adminlogout')
def admin_logout():
    session.clear()
    # redirect to a particular function name
    return redirect(url_for('admin_login'))

if __name__ == "__main__":
    app.run(port='5243',debug=True)



