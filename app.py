from flask import Flask, url_for, render_template, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "!@@#%#$%$^GVHGFcbcgfDFDd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def home():
    user = User.query.all()
    print(user)
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash("Login SuccessFully", "success")
            return redirect(url_for('home'))
        else:
            flash("User Dont' Match !", "danger")
            return render_template("login.html")
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 == password2:
            password = generate_password_hash(password1)
            user = User(username=username, password=password)
            if user is not None:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash("User None!")
                return render_template('signup.html')
        else:
            flash("Password Don't Match !", "danger")
            return render_template('signup.html')
    else:
        return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)