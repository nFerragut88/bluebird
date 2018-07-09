import os, redis
from app import app
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [Required()])
    submit = SubmitField('Submit')
    

# abspath = (os.path.abspath(os.curdir))
key = open('app/apiKey.txt').readline()

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
    
@app.route('/home')
def home():
    return render_template('home.html', my_string="nathan")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/project', methods=['GET','POST'])
def project():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        print('name', name, form.validate_on_submit())
    return render_template('project.html', form=form, name=name)

    
@app.route('/a')
def a():
    return render_template('infoWindow.html', key=key, 
    markers = [{'latitude':30, 'longitude':130, 'markerContent':'This is Uluru'},
    {'latitude':36, 'longitude':136, 'markerContent':'This is Osaka'}])
