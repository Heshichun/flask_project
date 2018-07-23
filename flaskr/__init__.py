import os
from flask import Flask
from flaskext.markdown import Markdown

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # 看一下instance_relative_config 的解释：默认为False，如果设置为True的话，他会将配置文件路径设置为实例文件的路径，而不是应用程序根目录
    Markdown(app)
    app.config.from_mapping(
        SECRET_KEY = 'DEV',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
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
    
    from . import db #防止循环调用
    db.init_app(app)#在工厂中导入并调用这个函数。

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint = 'index')
    #但是，下文的 index 视图的端点会被定义为 blog.index 。一些验证视图 会指定向普通的 index 端点。 我们使用 app.add_url_rule() 关联端点名称 'index' 和 / URL ，这样 url_for('index') 或 url_for('blog.index') 都会有效，会生成同样的 / URL 。
    return app