from flask import Flask,render_template,request,redirect
from secrets import token_hex
from random import choice,randint
from string import ascii_letters
import validators

app = Flask(__name__)
app.secret_key = token_hex(40)
print("secret_key:",app.secret_key)
host_name = None

shortcut = []
list_web = []

def shortname():
    n = ""
    for i in range(randint(3,6)):
        i = choice(ascii_letters)
        n = n+i
    return n

def create_link(shortname , value):
    shortcut.append(shortname)
    list_web.append(value)

@app.before_request
def Get_HostName():
    global host_name
    host_name = request.url


@app.route("/",methods=["GET","POST"])
def Index():
    if request.method == "POST":
        key = shortname()
        val = request.form.get("website",None)
        if validators.url(val):
            create_link(key,val)
            return render_template('index.html',key=key,val=val,host=host_name)
        else:
            msg = "لطفا آدرس وبسایت را درست وارد کنید http://mihan.ir"
            return render_template('index.html',key='Error',val='Error',msg=msg,host=host_name)
    if request.method == "GET":
        return render_template('index.html')

@app.route("/<name>")
def Move_to(name):
    return redirect(Fined_or_None(name))

@app.route("/v/<int:id>")
def View(id):
    if id==1:
        return list_web
    elif id==10:
        return f"{shortcut};{list_web}"
    else:
        return shortcut

def Fined_or_None(requesting:str):
    try:
        requesting = shortcut.index(requesting)
        requesting = list_web[requesting]
        return requesting
    except Exception:
        return None

if '__main__' in __name__:
    app.run(debug=True)