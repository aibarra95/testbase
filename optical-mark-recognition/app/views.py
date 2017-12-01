from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, StatForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Adrien'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/stats', methods=['GET','POST'])
def stats():
	form = StatForm()
	gt = 
	
	
