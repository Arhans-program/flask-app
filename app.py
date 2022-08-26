from flask import Flask,request,render_template,url_for
app = Flask(__name__)
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
    try:
      cheak_in_file = open(name+".txt","r")
    except FileNotFoundError:
      return render_template("error.html",name=name)
    if password in cheak_in_file.read():
      cheak_in_file.close()
      return render_template("existing.html",name=name)
    elif password not in cheak_in_file.read():
      return render_template("error.html",name=name)
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

@app.route("/signup",methods = ["GET","POST"])
def signup():
  name=""
  cheak_in_file = ""
  password = ""
  if request.method =="POST" and "create_username" in request.form and "create_password" in request.form:
    name=request.form.get("create_username")
    password=request.form.get("create_password")
    cheak_in_file=open(name+".txt","a+")
    cheak_in_file.close()
    cheak_in_file=open(name+".txt","w")
    cheak_in_file.write(password)
    cheak_in_file.close()
    return render_template("existing.html",name=name)
  return render_template("signup.html",name=name)
app.run()
