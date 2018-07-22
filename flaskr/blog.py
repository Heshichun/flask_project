from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)
#博客蓝图没有 url_prefix 。因此 index 视图会用于 / ， create 会用于 /create ，以此类推。

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts = posts)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):#check_author 参数的作用是函数可以用于在不检查作者的情况下获取一个 post 。
                                    #这主要用于显示一个独立的帖子页面的情况，因为这时用户是谁没有关系， 用户不会修改帖子。
                                    #这里可能有问题，怀疑会出现其他登录用户无法查看内容这样的情况。
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'# http://www.runoob.com/sqlite/sqlite-joins.html
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post


# @login_required
# def create_comments(id):
#     # if not title:
#     #     error = 'Title is required.'
#     # 以后再添加条件判断相关
#     body = request.form['comments_body']
#     db = get_db()
#     db.execute(
#         'INSERT INTO comments (post_id, body, author_id)'
#         ' VALUES (?, ?, ?)',
#         (id, body, g.user['id'])
#     )
#     db.commit()
#     return redirect(url_for('blog.view_post',values=id))

def get_comments(id):
    db = get_db()
    comments = db.execute(
        'SELECT id, body, created, author_id, post_id'
        ' FROM comments'# http://www.runoob.com/sqlite/sqlite-joins.html
        ' WHERE post_id = ?',
        (id,)#参数设置要注意格式
    ).fetchall()
    return comments

@bp.route('/<int:id>/update', methods = ('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post = post)

@bp.route('/<int:id>/delete',methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>', methods=('GET','POST'))
def view_post(id):

    if request.method == 'POST':
        # if not title:
        #   error = 'Title is required.' 以后再添加
        body = request.form['comments_body']
        db = get_db()
        db.execute(
            'INSERT INTO comments (post_id, body, author_id)'
            ' VALUES (?, ?, ?)',
            (id, body, g.user['id'])
        )
        db.commit()
        return redirect(url_for('blog.view_post', id = id))
        #url_for 函数关于生成动态地址的用法https://blog.csdn.net/bestallen/article/details/52107944
    else:
        post = get_post(id)
        comments = get_comments(id)
        return render_template('blog/post.html', post=post, comments=comments)