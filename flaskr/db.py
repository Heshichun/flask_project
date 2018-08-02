import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext #这是干什么的？

def get_db():
    if 'db' not in g:
        #g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存 可能多个函数都会用到的数据。
        g.db = sqlite3.connect( #建立一个数据库连接，该连接指向配置中的 DATABASE 指定的文件。
            current_app.config['DATABASE'],
            #current_app 是另一个特殊对象，该对象指向处理请求的 Flask 应用。
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #告诉连接返回类似于字典的行，这样可以通过列名称来操作 数据。
    return g.db

def close_db(e=None): #close_db 通过检查 g.db 来确定连接是否已经建立。如果连接已建立，那么 就关闭连接。
    db = g.pop('db' , None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))
    #open_resource() 打开一个文件，该文件名是相对于 flaskr 包的。get_db 返回一个数据库连接，用于执行文件中的命令。

@click.command('init-db')#click.command() 定义一个名为 init-db 命令行，它调用 init_db 函数，并为用户显示一个成功的消息。
@with_appcontext # ??
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

#close_db 和 init_db_command 函数需要在应用实例中注册，否则无法使用。 我们写一个函数，把应用作为参数，在函数中进行注册。
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)