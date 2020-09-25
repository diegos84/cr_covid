import os
import sqlite3
import csv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from application import app, db, bcrypt
from application.models import Users
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, LicensePlate
from application.handlers import error_403, error_404, error_500
from application.utils import send_reset_email, api_call, all_countries, get_the_news
from flask_login import login_user, current_user, logout_user, login_required

# COMMENT-OUT LIST, NOT RELEVANT SINCE LAST POLICY CHANGE BY THE GOVERNMENT
# cantons = []    
# with open('application/static/cantons.csv', newline='') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     cantons = list(csv_reader)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
  # Use functions containing data from API call for select dropdown on GET method and user query on POST method
  if request.method == "GET":
      countries = all_countries()
      cr_covid = api_call('CRI')
      return render_template('index.html', title='Home', cr_covid=cr_covid, countries=countries)
  cr_covid = api_call('cri')
  country = request.form.get('choose_country')
  country_covid = api_call(country)
  articles = get_the_news()
  return render_template('index.html', title='Home', cr_covid=cr_covid, country_covid=country_covid, country=country, articles=articles)
  
    

@app.route("/register", methods=["GET", "POST"])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account {form.username.data} created! Now you can log in', 'primary')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)     


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid email and/or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()                                                                                                                                                                                   
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully!', 'primary')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account Changes', form=form)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with instructions has been sent to help you reset your password', 'primary')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash('Your token is invalid or expired', 'danger')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! Now you can log in', 'primary')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/transportation", methods=["GET", "POST"])
@login_required
def transportation():
    form = LicensePlate()
    even = [0, 2, 4, 6, 8]
    odd = [1, 3, 5, 7, 9]
    if form.validate_on_submit():
        plate = int(form.digits.data)
        return render_template('transportation.html', title='Transportation', plate=plate, form=form, even=even, odd=odd)
    return render_template('transportation.html', title='Transportation', form=form)


@app.route("/news")
@login_required
def news():
    news = get_the_news()
    return render_template('news.html', title='News', news=news)


@app.route("/stats", methods=["GET", "POST"])
@login_required
def stats():
  # Use functions containing data from API call for select dropdown on GET method and user query on POST method
  if request.method == "GET":
      countries = all_countries()
      return render_template('stats.html', title='Stats', countries=countries)
  countries = all_countries()
  cr_covid = api_call('cri')
  country = request.form.get('choose_country')
  country_covid = api_call(country)
  return render_template('stats.html', title='Stats', cr_covid=cr_covid, country_covid=country_covid, countries=countries, country=country)
