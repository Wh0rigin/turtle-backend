import os

from flask import Flask
from flask import request
from . import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
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
    @app.route('/UserProfile',methods=[ 'GET' , 'POST' , 'PUT' , 'DELETE' ])
    def get_name():

        #GET handler
        if request.method == 'GET' :
            uid = request.args.get('id',1)
            # 1. connect sql
            # This is a happy path
            sqlcmd = "select * from userProfile where id={}".format(uid)
            
            result = db.query(sqlcmd)

            if result is None:
                return dict(msg='Data not found')
            else:
                return result

        #POST handler
        elif request.method == 'POST':
            username = request.json.get('username')
            msg = request.json.get('msg')
            #TODO 检查是否有相同名称的数据
            sqlcmd = "insert into userProfile (username,msg) values ('{}',{})".format(username,msg)
            result = db.execution(sqlcmd)
            if result is None:
                return dict(msg="Errno")
            else:
                return result

        #DELETE handler
        elif request.method == 'DELETE':
            id = request.json.get('id')
            sqlcmd = "delete from userProfile where id = {}".format(id)
            result = db.execution(sqlcmd)
            return dict(successs=True)

        #PUT handler
        elif request.method == 'PUT':
            id = request.json.get('id')
            username = request.json.get('username')
            msg = request.json.get('msg')
            sqlcmd = "update userProfile set username='{}',msg={} where id={}".format(username,msg,id)
            result = db.execution(sqlcmd)
            return dict(successs=True)
            
    return app