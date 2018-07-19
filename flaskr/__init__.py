import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # 看一下instance_relative_config 的解释：默认为False，如果设置为True的话，他会将配置文件路径设置为实例文件的路径，而不是应用程序根目录
    app.config.from_mapping(
        SECRET_KEY = 'DEV'
        DATEBASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if  test_config is None:
        app.config.from_pyfile('config.py' , silent=True)
    else:
        app.config.from_mapping('test_config.py')

    try:
        os.makedirs(app.instance_path)
        #os.makedirs() 可以确保 app.instance_path 存在。因为 datebase 保存在这个目录下，因此必须保证其存在。
    except OSError:
        pass
    
    @app.route('/')
    def hello():
        return 'Hello World'
    
    return app