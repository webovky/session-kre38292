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

def login_required(f):
    def wrapper(*args, **kwargs):
        if "user" in session:
            return f(*args, **kwargs)
        else:
            flash(
                f"Pro zobrazení této stránky ({request.path}) je nutné se přihlásit!",
                "err",
            )
            return redirect(url_for("login", next=request.path))
    wrapper.__name__=f.__name__
    wrapper.__doc=f.__doc__
    return wrapper

@app.route("/abc/", methods=["GET"])
@login_required
def abc():
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
    if "user" in session:
        return render_template("kvetak.html.j2")
    else:
        flash(f"Nejsi přihlášen (nebo neočkván), pro zobrazení ({request.path}) je nutné se přihlásit.","err")
        return redirect(url_for("login",next=request.path))

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
    next=request.args.get("next")
    if login == "lofas" and password == "dingus":
        session["user"]=login
        flash("A jsme doma","pass")
        if next:
            return redirect(next)
    else:
        flash("Přístup zamítnut, bohužel no, zkus to znova.","err")
    if next:
        return redirect(url_for("login"), next=next)
    else:
        return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    session.pop("user",None)
    flash("Tak já jdu.","pass")
    return redirect(url_for("login"))
