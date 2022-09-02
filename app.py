from flask import Flask,request,render_template,url_for,session,redirect,flash
app = Flask(__name__)
app.secret_key = "hello"
@app.route("/signup",methods = ["GET","POST"])
def signup():
  name=""
  cheak_in_file = ""
  password = ""
  if request.method =="POST" and "create_username" in request.form and "create_password" in request.form:
    name=request.form.get("create_username")
    password=request.form.get("create_password")
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
  cheak_in_file = ""
  password = "" 
  receiver = ""
  mesage = ""
  if request.method == "POST" and "username" in request.form and "password" in request.form:
    name=request.form.get("username")
    password=request.form.get("password")
    session["user"] = name
    session["enter"] = password
    try:
      cheak_in_file = open(name+".txt","r")
    except FileNotFoundError:
      return render_template("main.html",name=name)
    if password in cheak_in_file.read():
      cheak_in_file.close()
      name = session["user"]
      return render_template("existing.html",name=name)
    elif password not in cheak_in_file.read():
      return render_template("main.html",name=name)
  if request.method == "POST" and "sms" in request.form and "receiver" in request.form:
    receiver=request.form.get("receiver")
    mesage=request.form.get("sms")
    m = open("message.txt","a+")
    m.close()
    m = open("message.txt","a")
    m.write("\n"+receiver+" ")
    m.write(mesage)
    m.close()
    return render_template("existing.html",name=name)
  return render_template("login.html",name=name)
  
@app.route("/profile",methods = ["GET","POST"])
def profile():
  if "user" in session and "enter" in session: 
   name = session["user"]
   password = session["enter"]
   return render_template("profile.html",name=name,password=password)
  elif "user" not in session and "enter" not in session:
    return redirect(url_for("signup"))
  elif request.method == "POST" and "home" in request.form:
    name = session["user"]
    return render_template("existing.html",name=name)

@app.route("/existing",methods = ["GET","POST"])
def existing():
  name=""
  if "user" in session:
    name = session["user"]
    return render_template("existing.html",name=name)
  else:
    return render_template("login.html")

app.run(host="0.0.0.0")
