from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course, User
from flask_migrate import Migrate
from flask_login import LoginManager


from flask_ckeditor import CKEditor

def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_viem = 'front.login'


def register_ckeditor(app):
    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['CKEDITOR_FILE_UPLOADER'] = 'upload_for_ckeditor'

    CKEditor(app)
    #ckeditor.init_app(app)


def create_app(config):

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456"
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    register_ckeditor(app)
    return app

