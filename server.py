from flask import Flask,render_template

app = Flask(__name__) #constructing app object

books =[{'bid':111,'title':'Java Springboot framework','author':'S John'},{'bid':112,'title':'Maths for Data Science','author':'Edison'},{'bid':113,'title':'Deep Learning with Tensorflow','author':'David'}]

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html',tit="Book Info",booksKey = books)


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



if __name__ == "__main__":
    app.run(port='5243',debug=True)



