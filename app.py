from flask import Flask,request,render_template,url_for,session,redirect,flash
import sqlite3
app = Flask(__name__)
app.secret_key = "hello"

@app.route("/existing",methods = ["GET","POST"])
def existing():
  name = session["user"]
  con = sqlite3.connect('message.db')
  cur = con.cursor()
  cur.execute("SELECT * FROM messaging where reciever == (?)", (name,))
  items = cur.fetchall()
  con.commit()
  con.close()
  return render_template("existing.html",name=name, messages=items)

@app.route("/logout",methods = ["GET","POST"])
def logout():
  session.pop('user')
  session.pop('enter')
  return redirect(url_for('login'))

@app.route("/signup",methods = ["GET","POST"])
def signup():
  name=""
  cheak_in_file = ""
  password = ""
  if request.method =="POST" and "create_username" in request.form and "create_password" in request.form:
    name=request.form.get("create_username")
    password=request.form.get("create_password")
    session["user"] = name
    session["enter"] = password
    try:
      cheak_in_file = open(name+".txt","r")
      flash('Username alredy exists')
    except FileNotFoundError:
      cheak_in_file=open(name+".txt","a+")
      cheak_in_file.close()
      cheak_in_file=open(name+".txt","w")
      cheak_in_file.write(password)
      cheak_in_file.close()
      return render_template("existing.html",name=name)
  return render_template("signup.html",name=name)

@app.route("/login",methods = ["GET","POST"])
def login():
  name=""
  password = "" 
  receiver = ""
  mesage = ""
  rm = ""
  if request.method == "POST" and "username" in request.form and "password" in request.form:
    name=request.form.get("username")
    password=request.form.get("password")
    session["user"] = name
    session["enter"] = password
    con = sqlite3.connect('message.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM messaging where reciever == (?)", (name,))
    items = cur.fetchall()
    con.commit()
    con.close()
    return render_template("existing.html",name=name, messages=items)
  if request.method == "POST" and "sms" in request.form and "receiver" in request.form:
    receiver=request.form.get("receiver")
    mesage=request.form.get("sms")
    con = sqlite3.connect('message.db')
    cur = con.cursor()
    sender = session["user"]
    rm = [(receiver,sender,mesage)]
    cur.executemany("INSERT INTO messaging VALUES (?,?,?)",rm)
    con.commit()
    con.close()
    name = session["user"]
    con = sqlite3.connect('message.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM messaging where reciever == (?)", (name,))
    items = cur.fetchall()
    con.commit()
    con.close()
    return render_template("existing.html",name=name, messages=items)
  return render_template("login.html",name=name)

@app.route("/profile",methods = ["GET","POST"])
def profile():
  if "user" in session and "enter" in session: 
   name = session["user"]
   password = session["enter"]
   return render_template("profile.html",name=name,password=password)
  elif "user" not in session and "enter" not in session:
    return redirect(url_for("signup"))

app.run(host="0.0.0.0")