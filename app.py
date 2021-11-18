from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
"""
    secret_key se generuje nejlépe pomocí os.random(24)
    ale obecně je to prostě velké náhodné číslo
    proměnnou secret_key nikdy nikdy nikdy nikdy nesdílím v repozitáři!!!!!!!
"""
app.secret_key = b'\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0'b'\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0'


@app.route("/")
def index():
    return render_template("base.html.j2", a=12, b=3.14)


@app.route("/abc/", methods=["GET"])
def abc():
    session['user'] = 'karel'
    try:
        x = request.args.get("x") 
        y = request.args.get("y")
        soucet = int(x) + int(y)
    except TypeError:
        soucet = None
    except ValueError:
        soucet = "Nedělej si srandu!!!"
    
    slovo = request.args.get('slovo')
    if slovo:
        session['slovo'] = slovo

    return render_template("abc.html.j2", soucet=soucet)


@app.route("/abc/", methods=["POST"])
def abc_post():

    jmeno = request.form.get("jmeno")
    heslo = request.form.get("heslo")
    print("POST:", jmeno, heslo)

    return redirect(url_for("abc"))


@app.route("/banany/<parametr>")
def banany(parametr):
    return render_template("banany.html.j2", parametr=parametr)


@app.route("/kvetak/")
def kvetak():
    return render_template("kvetak.html.j2")

@app.route("/Login/", methods=("GET",))
def login():
    if request.method == "GET":
        login = request.args.get("login")
        password = request.args.get("password")
    return render_template("login.html.j2")

@app.route("/Login/", methods=("POST",))
def login_post():
    login = request.form.get("login")
    password = request.form.get("password")
    print(login,password)
    if login == "lofas" and password == "dingus":
        session["user"]=login
        flash("You son of a b*tch your in","pass")
    else:
        flash("Acces denied","err")
    return redirect(url_for("login"))
