import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth' , __name__ , url_prefix='/auth')
#和应用对象一样， 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 url_prefix 会添加到所有与该蓝图关联的 URL 前面。

#准备开始写视图

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        db = get_db()
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        #fetchone() 根据查询返回一个记录行。 如果查询没有结果，则返回 None 。后面还用到 fetchall() ，它返回包括所有结果的列表。


        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
            #如果验证成功，那么在数据库中插入新用户数据。
            #为了安全原因，不能把密码明文 储存在数据库中。
            #相代替的，使用 generate_password_hash() 生成安全的哈希值并储存 到数据库中。
            #查询修改了数据库是的数据后使用 meth:db.commit() <sqlite3.Connection.commit> 保存修改。
        flash(error)
        #如果验证失败，那么会向用户显示一个出错信息。 flash() 用于储存在渲染模块时可以调用的信息。

    return render_template('auth/register.html')
    #当用户最初访问 auth/register 时，或者注册出错时，应用显示一个注册 表单。 render_template() 会渲染一个包含 HTML 的模板。

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            #check_password_hash() 以相同的方式哈希提交的 密码并安全的比较哈希值。如果匹配成功，那么密码就是正确的。
            error = 'Incorrect password.'

        if error is None:
            #session 是一个 dict ，它用于储存横跨请求的值。当验证 成功后，用户的 id 被储存于一个新的会话中。
            #会话数据被储存到一个 向浏览器发送的 cookie 中，在后继请求中，浏览器会返回它。 Flask 会安全对数据进行 签名 以防数据被篡改
            session.clear()
            session['user_id'] = user['id']
            #现在用户的 id 已被储存在 session 中，可以被后续的请求使用。
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_loggged_in_user():
    #bp.before_app_request() 注册一个 在视图函数之前运行的函数，不论其 URL 是什么。 load_logged_in_user 检查用户 id 是否已经储存在 session 中，并从数据库中获取用户数据，然后储存在 g.user 中。 g.user 的持续时间比请求要长。 如果没有用户 id ，或者 id 不存在，那么 g.user 将会是 None 。
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    
@bp.route('/logout')
def logout():
    # 注销的时候需要把用户 id 从 session 中移除。 然后 load_logged_in_user 就不会在后继请求中载入用户了。
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    # 装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。新的函数检查用户 是否已载入。
    # 如果已载入，那么就继续正常执行原视图，否则就重定向到登录页面。 我们会在博客视图中使用这个装饰器。
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view