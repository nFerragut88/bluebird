import os, redis, sys
from app import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required
from werkzeug import secure_filename
from flask import session
from flask import Flask
from flask import Session
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_dropzone import Dropzone

dropzone = Dropzone(app)
app.config.update(
    UPLOADED_PATH=os.path.join('C:/Users/Nathan/Documents/GitHub/bluebird/app/users/coolman', 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [Required()])
    submit = SubmitField('Submit')
    
class CreateForm(FlaskForm):
    name = StringField('Username:', validators = [Required()])
    password = PasswordField('Password:',validators = [Required()])
    submit = SubmitField('Submit')
class LoginForm(FlaskForm):
    name = StringField('Username:', validators = [Required()])
    password = PasswordField('Password:',validators = [Required()])
    submit = SubmitField('Submit')
class CreateProject(FlaskForm):
    name = StringField('Project Name:', validators = [Required()])
    submit = SubmitField('Submit')

redis_db = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
# abspath = (os.path.abspath(os.curdir))
key = open('app/apiKey.txt').readline()
@app.route('/')
@app.route('/index')
def index():
    
    return "Hello, World"
@app.route('/upload')
def upload():
    
    return render_template('upload.html', form=form)
# @app.route('/set/')
# def set():
    # session['key'] = 'value'
    # return 'ok'

# @app.route('/get/')
# def get():
    # counter = ""
    # for i in session:
        # counter+= i
    # if 'coolman' in session:
        # return "success"
    # return counter
    # return session.get('key', 'not set')
    
@app.route('/home', methods=['GET','POST'])
def home():
    name = ""
    form = CreateForm()
    loginForm = LoginForm()
    
    if loginForm.validate_on_submit():
        if (str(redis_db.get(loginForm.name.data))[2:len(str(redis_db.get(loginForm.name.data)))-1] == str(loginForm.password.data)):
            name = "welcome,",loginForm.name.data
            
            session[loginForm.name.data] = loginForm.name.data
            return render_template('home.html', my_string="successful login", form=form, loginForm=loginForm)
        else:
            redispass = str(redis_db.get(loginForm.name.data))
            yourpass = str(loginForm.password.data)
            failure = "redispass:"+redispass+"\nyourpass:"+yourpass
            return "failure"
        
    if form.validate_on_submit() and redis_db.get(form.name.data) == None:
        name = form.name.data
        password = form.password.data
        redis_db.set(name, password)
        form.name.data = ''
        form.password.data = ''
        path = "C:/Users/Nathan/Documents/GitHub/bluebird/app/users/"+name
        os.mkdir(path)
        name = "hello, "+name
        print('name', name, form.validate_on_submit())
        
    elif redis_db.get(form.name.data)!=None:
        name = "Error, account already exists"
    
    return render_template('home.html', my_string=name, form=form, loginForm=loginForm)
    
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects', methods = ['GET', 'POST'])
def projects():
    createProject = CreateProject()
    if createProject.validate_on_submit():
        global tempName 
        tempName = str(createProject.name.data)
        print("set name",tempName)
        name = next(iter(session.values()))
        path = "C:/Users/Nathan/Documents/GitHub/bluebird/app/users/"+str(name)
        path += "/"+tempName+"/"
        path = str(path)
        try:
            os.mkdir(path)
        except:
            pass
    if request.method == 'POST':
        for key, f in request.files.items():
            name = next(iter(session.values()))
            path = "C:/Users/Nathan/Documents/GitHub/bluebird/app/users/"+str(name)
            path += "/"+tempName
            print(path)
            if key.startswith('file'):
                f.save(os.path.join(path, f.filename))
    return render_template('projects.html', createProject = createProject)

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
