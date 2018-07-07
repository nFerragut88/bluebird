from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

from app import views

 
