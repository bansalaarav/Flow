from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib, ssl


app = Flask(__name__)


app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^AAAAAAAAAAAAAAAAAAA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    played_quiz = db.Column(db.Boolean, default=False)
    best_score = db.Column(db.Integer, default=0)
    best_time = db.Column(db.Float, default=0)



def message(receiver_name, name, email, message):
    return f"""
Greetings from FLOW, {receiver_name}!

Someone wants to get in touch! These are the details of the sender:

Name: {name}
Email: {email}
Message: {message}  
      """


def email_person(name, email, _message):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "bansalaarav2007@gmail.com"
    password = "lgtxnfriwjkbypnu"

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)  # Secure the connection
        server.login(sender_email, password)

        server.sendmail(sender_email, "shreyasdeo.k50@gmail.com",
                        message("Shreyas", name, email, _message))
        server.sendmail(sender_email, "bansalaarav2007@gmail.com",
                        message("Aarav", name, email, _message))
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

@app.route("/", methods=['GET', "POST"])
def index():
    
    if session.get("logged-in"):
        return redirect(url_for("dashboard"))
    else:
        if request.method == "POST":
            full_name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")
            email_person(full_name, email, message)
            flash("Email sent successfully!")
        return render_template("index.html")

@app.route("/terms-of-use/")
def terms_of_use():
    return render_template("term-of-use.html")

@app.route("/privacy-policy/")
def privacy_policy():
    return render_template("privacy-policy.html")


@app.route("/blog/")
def blog():
    return render_template("blog-page.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/dashboard/")
def dashboard():
    if session.get("logged-in"):
        num_of_ppl = 0
        best_times = []
        users = User.query.all()
        email = session["email"]
        user_ = User.query.filter_by(email=email).first()
        user_bs = user_.best_score
        user_bt = user_.best_time
        for user in users:
            if user.played_quiz:
                num_of_ppl += 1
            if user.best_time != 0:
                best_times.append(user.best_time)
        if best_times:
            val = round(min(best_times), 1)
        else:
            val = 0

        return render_template("dashboard.html", num_of_ppl=num_of_ppl, best_time=val, user_bs=user_bs, user_bt=round(user_bt, 1))
    else:
        return redirect(url_for("login"))

@app.route("/quizzes/")
def quizzes():
    if session.get("logged-in"):
        scores = {}
        users = User.query.all()
        for user in users:
            if user.best_time == 0:
                pass
            else:
                v = user.best_score/user.best_time
                scores[f"{user.first_name} {user.last_name}"] = v
        if scores:
            # temp = None
            # num_of_sames = 0
            # for score in scores:
                
            #     if score == temp:
            #         same = scores.index(score) + 1
            #         num_of_sames += 1
            #     else:
            #         temp = score
            res = sorted(scores, key = lambda x: x[1], reverse=True)[:5]
        else:
            res = []
       
        
        return render_template("quizzes.html", people=res)
    else:
        return redirect(url_for("login"))

@app.route("/quizzes/<variable>/")
def quizzes_(variable):
    if session.get("logged-in"):
        if variable == "quiz-1":
           return render_template("quizzes/quiz-1.html")
        elif variable == "quiz-2":
            return render_template("quizzes/quiz-2.html")
        else:
            return redirect(url_for("quizzes"))
    else:
        return redirect(url_for("login"))

@app.route("/user-played-quiz", methods=["POST"])
def user_played_quiz():
    time_ = round(60 - float(request.form["_time"]), 1)
    print(time_)
    score = int(request.form["_score"]) # 10 or 7 or 2
    email = session["email"]
    user = User.query.filter_by(email=email).first()
    if not user.played_quiz:
        user.played_quiz = True
        db.session.commit()
    if user.best_score < score:
        user.best_score = score
        user.best_time = time_
        db.session.commit()
    elif user.best_score == score:
        if user.best_time > time_:
            user.best_time = time_
            db.session.commit()
        
    return "None"

@app.route("/blog/<variable>/")
def blog_pages(variable):
    if variable == "history-of-drone-tech":
        return render_template("blogs/blog-1.html")
    elif variable == "how-do-drones-work":
        return render_template("blogs/blog-2.html")
    elif variable == "drones-and-covid-19":
        return render_template("blogs/blog-3.html")
    elif variable == "drones-and-sdgs":
        return render_template("blogs/blog-4.html")

    return redirect(url_for("blog"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):

                session["logged-in"] = True

                session['email'] = user.email

                session['first_name'] = user.first_name
                flash('Login successful!')
                print("login successful")
                return redirect(url_for("dashboard"))
            else:
                flash('Incorrect password!')
                return redirect(url_for("login"))
        flash('Email does not exist!')
        print("Email does not exist!")
        return redirect(url_for("login"))
    if session.get("logged-in"):
        print("logged in")
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")


@app.route('/logout/')
def logout():
    session["logged-in"] = False
    flash("Logged out successfully!")
    return redirect(url_for('index'))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        user = User.query.filter_by(email=email).first()

        if not user:

            if password == confirm_password:
                hashed_password = generate_password_hash(password, method='sha256')
                new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful!")

                session["logged-in"] = True

                session['email'] = new_user.email

                session['first_name'] = new_user.first_name
                print("reg success")
                return redirect(url_for("dashboard"))
            else:
                flash("Passwords do not match!")
                return redirect(url_for("register"))
        else:
            flash("An account with that email already exists!")
            return redirect(url_for("register"))
    if session.get("logged-in"):
        print("reg logged in")
        return redirect(url_for("dashboard"))

    return render_template("register.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
