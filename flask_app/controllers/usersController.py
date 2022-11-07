from flask_app import app
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index ():
    return render_template('login.html')

@app.route('/reg')
def newuser():
    return render_template('users.html')


@app.route('/register/user', methods = ['POST'])
def register ():
    if not User.validate(request.form):
        return redirect('/reg')  # back to login page
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    
    id = User.register(data)
    session['user_id'] = id
    session['username'] = data['first_name']
    print('session', session)
    return redirect(f'/dashboard')


# Login User route with post method form, lets users login #
@app.route('/login/user', methods = ['POST'])
def login ():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect ('/dashboard')


# Route that shows the dashboard get's one user #
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")
    data = {'id': session['user_id']}
    return render_template('dashboard.html', user = User.get_one(data),recipies = Recipe.get_user_with_recipe())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
