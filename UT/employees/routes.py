from flask import render_template, Blueprint


employees = Blueprint("employees", __name__)


@employees.route('/login')
def login():
    return 'Hello World'