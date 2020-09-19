from flask import Flask, request, Blueprint, render_template, redirect, session

# create a blueprint
bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    if request.method == 'GET':
        # print("Is logged in?", session['is_logged_in'])
        return render_template('index.html')
