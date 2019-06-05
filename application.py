import os

from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/postgres')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/res" , methods=["post","get"])
def res():
    name=request.form.get("name") 
    if not name:
        return render_template("err.html",massage="plase enter the name")
    pw=request.form.get("password") 
    if not pw:
        return render_template("err.html",massage="plase enter the password")
    if db.execute("select * from members where name like :name", {"name":name}).rowcount==0 :
        db.execute("insert into members(name,password) values (:name,:password)",{"name":name,"password":pw})
        db.commit()
        return render_template("index.html",massage="register successfully,please sign in")
    else:
        return render_template("err.html",massage="username has been used")
     
@app.route("/book", methods=["POST"])
def book():

    name=request.form.get("name") 
    if not name:
        return render_template("err.html",massage="plase enter the name")
    pw=request.form.get("password") 
    if not pw:
        return render_template("err.html",massage="plase enter the password")
    if db.execute("select * from members where name like :name and password=:password", {"name":name,"password":pw}).rowcount==1 :
        return redirect('/success')
    else:
        return render_template("err.html",massage="invaild name or password")

    
@app.route("/success", methods=["post","get"])
def success():
    if request.method=="POST" :
        
            name=request.form.get("name")
            if not name:
                return render_template("success.html",massage="please enter book")
            books= db.execute(f"select * from books where title like '%{name}%'").fetchall()
            
    else:
        return render_template("success.html")
        
    if not books:
        return render_template("success.html",massage="can't find any book")
    else :
        return render_template("success.html",books=books)

    
