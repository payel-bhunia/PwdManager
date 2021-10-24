from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    env = 'dev'
    if env == 'dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kiran@localhost:5433/pwdmng'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vcektifmkqivgi:cd142c9f4ea504b9e8c993799ef01e31368858dd4da71f1b6976393f4ee4f157@ec2-3-209-65-193.compute-1.amazonaws.com:5432/d7cls68s9h2c1h'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, UserURL

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    db.create_all(app=app)
    print('Created Database!')
