from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash,Blueprint
from forms import LoginForm
from . import admin

@admin.route('/')
def index():
    return '<h1>Hello World!</h1>'

@admin.route('/1')
def index2():
    return redirect(url_for('.index'))

@admin.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('logged in')
            return redirect(url_for('.index'))
    return render_template('login.html', error=error)

@admin.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('admin.index'))

@admin.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.excute('insert into entries (title, text) values (?, ?)',[request.form['title'],request.form['text']])

    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('admin.index'))