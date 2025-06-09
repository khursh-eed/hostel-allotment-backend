from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from app import admin
from . import auth  # important - imports the blue print instance
# blueprint instance is important to use @auth.route decorator 
from .forms import LoginForm, RegisterForm 





@auth.route('/testlogin')
def testlogin():
    return "<h1>Login route works!</h1>"



@auth.route('/login', methods=['GET', 'POST'])
def login():
    from app.models import User
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # we login the user
            login_user(user)
            flash("Logged in successfully!", "success")
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid email or password", "danger")
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    from app.models import User
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered", "warning")
            return redirect(url_for('auth.register'))
        
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            # we're hashing the password given before storing it in our db so that even if anyone hack our db they dont get acces to anything
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))
    # return "<p>register</p>"
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
# this will directly take us to login if not logged in
def logout():
    from app.models import User
    logout_user(User)
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))

from . import routes 
