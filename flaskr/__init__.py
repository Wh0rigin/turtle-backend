import os

from flask import Flask
from flask import request

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello_world():
        return 'Hello world'

    # a simple page that get user msg
    @app.route('/UserProfile',methods=['GET','POST'])
    def get_name():
        name = request.args.get('name','')

        if name == 'Wh0rigin' :
            return dict(name='Wh0rigin')
        else:
            return dict(name='Another')

    return app