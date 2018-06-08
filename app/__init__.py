from flask import Flask
import sqlite3
from config import config
from flask import Blueprint

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    from main.admin import admin
    app.register_blueprint(admin)

    return app

#__init__.py里面创建实例,应用实例对象创建完再引入视图函数的模块,因为这时候视图函数上的@app.route()才有效