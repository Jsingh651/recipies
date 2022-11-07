from flask_app import app
from flask import Flask, redirect, session, request, render_template, url_for, flash
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
from flask_app.controllers import usersController

@app.route('/show/page')
def shwocrete():
    if 'user_id' not in session:
        flash("You must be logged in to create a recipe.")
        return redirect("/")
    return render_template('create_recipe.html')

@app.route('/create/recipe', methods = ['POST'])
def create_recpipe():
    if not Recipe.validate_recipes(request.form):
        return redirect('/show/page')
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],   
        'description':request.form['description'],
        'instructions': request.form['instructions'],
        'cook_time': request.form['cook_time']
    }
    Recipe.create_recipes(data)
    return redirect('/dashboard')

@app.route('/show/recipe/<int:id>')
def get_recipe(id):
    if 'user_id' not in session:
        flash("You must be logged in to access the recipe.")
        return redirect("/")
    data = {'id': id}
    sessiondata = {'id': session['user_id']}
    userinfo = User.get_one(sessiondata)
    return render_template('showrecipe.html',
    recipie = Recipe.get_one_recipes(data), 
    userinfo = userinfo,recipies = Recipe.get_user_with_recipe())


@app.route('/edit/recipe/<int:id>')
def edit(id):
    if 'user_id' not in session:
        flash("You must be logged in to access the edit form.")
        return redirect("/")
    data = {'id':id}
    recipie = Recipe.get_one_recipes(data)
    return render_template('edit.html',recipie =recipie)

@app.route('/update/recipe', methods = ['POST'])
def update():
    if not Recipe.validate_recipes(request.form):
        return redirect('/show/page')
    data = {
        'recipie_id': request.form['recipie_id'],
        'name': request.form['name'],   
        'description':request.form['description'],
        'instructions': request.form['instructions'],
        'cook_time': request.form['cook_time']
    }
    Recipe.update_recipes(data)
    return redirect('/dashboard')


@app.route('/delete/<int:id>')
def delete(id):
    data = {'id':id}
    Recipe.delete(data)
    return redirect('/dashboard')