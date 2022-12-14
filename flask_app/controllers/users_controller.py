from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app import app

# Import models
from flask_app.models.user_model import User

bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/users')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def user_view():
    if 'user_id' not in session:
        return redirect('/')
    id_value = {
        'id': session['user_id']
    }
    one_user = User.get_by_id(id_value)
    return render_template('view.html', one_user=one_user)


@app.route('/users/new', methods=['post'])
def user_new():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
    }
    if not User.validate(data):
        return redirect('/')
    if not data['password'] == request.form['confirm_password']:
        flash("Passwords must match", "reg")
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(data['password'])
    session['user_id'] = User.new_user(data)
    return redirect('/dashboard')


@app.route('/users/login', methods=['POST'])
def user_login():
    data = {
        'email': request.form['signin_email']
    }
    one_user = User.get_by_email(data)
    if not one_user:
        flash("Invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['signin_password']):
        flash("Invalid credentials", "log")
        return redirect('/')
    session['user_id'] = one_user.id
    return redirect('/dashboard')


@app.route('/users/logout')
def end_session():
    del session['user_id']
    return redirect('/')
