'''
auth.py
Authenticates all user signups and logins and commites to the database
'''
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import *
from .variables import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login(): # Login
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() 
        if user: # Checks if the user already exists
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True) # If true, logs in the user
                return redirect(url_for('views.home')) # And lets them view the home page
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email doesn\'t exist!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout(): # Logout
    logout_user()
    return redirect(url_for('auth.login')) # Redirects to the login page

@auth.route('sign-up', methods=['GET', 'POST'])
def sign_up(): # Sign up 
    form = CreateUserForm()
    form.interest.choices = INTERESTS
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        experience = request.form.get('experience')
        affiliation = request.form.get('affiliation')
        interest = request.form.getlist('interest')

        if age == '':
            age = 0
        if affiliation == '':
            affiliation = None
        
        user = User.query.filter_by(email=email).first()

        #print(email, first_name, password1, password2, last_name, age, experience, affiliation, interest)

        if user: 
            flash('Email already exists!', category='error') # If the user already exists
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error') # A bunch of other checks
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(
                email=email, 
                password=generate_password_hash(password1, method='sha256'), 
                first_name=first_name,
                last_name=last_name,
                age=age,
                experience=experience,
                affiliation=affiliation,
                interest=interest)           
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user, form=form)
