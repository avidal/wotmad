# -*- coding: utf-8 -*-

from flask import Flask

from flask.ext.security import SQLAlchemyUserDatastore

from .core import db, security
from .helpers import register_blueprints
from .middleware import HTTPMethodOverrideMiddleware
from .models import User, Role


def create_app(package_name, package_path, settings_override=None,
               register_security_blueprint=True):

    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('wotmad.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    db.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=register_security_blueprint)

    register_blueprints(app, package_name, package_path)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app
