#!C:/python34/python.exe
import sys
import os
path = os.path.dirname(os.path.join(os.path.realpath(__file__), "../../"))
sys.path.insert(0, path)

from flask import Flask
from pywdbms.core.app import blueprint
from pywdbms.core.database import db_session, init_db

app = Flask(__name__)
app.secret_key = 'some_secret'
app.register_blueprint(blueprint)
app.config['DEBUG'] = True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
app.run()