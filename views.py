from app import app
from flask import render_template

key = open('/home/ubuntu/workspace/app/apiKey').readline()

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
#nathan go away no
@app.route('/a')
def a():
    return render_template('infoWindow.html', key=key, 
    markers = [{'latitude':30, 'longitude':130, 'markerContent':'This is Uluru'},
    {'latitude':36, 'longitude':136, 'markerContent':'This is Osaka'}])