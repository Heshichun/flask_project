from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash,Blueprint
from forms import LoginForm
from . import main

main = Blueprint('main' , __name__)

@main.route('/')
def index():
    return '<h1>Hello World!</h1>'
