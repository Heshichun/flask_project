# 网站搭建日志
### TODO：

- 分布显示索引。每页显示只显示五个帖子。
- 帖子可以上传图片。

- 美化
- 标签
- 各种路径问题
- Bootstrap
- 一个新帖子的 RSS 源


#### 7月25日
编辑页面也加了 markdown，但是有一个 必须要有 title 框的这样一个 bug 存在。解决方案是，想法获取 body 的第一行作为标题。

#### 7月23日
实现了 markdown。
[https://www.cdxy.me/?p=719](https://www.cdxy.me/?p=719)


#### 7月22日
今天实现了评论功能，整体涉及到了 sqlite3的外键以及一些 jinja 模板的问题。
```python
def get_comments(id):
	db = get_db()
	comments = db.execute(
		'SELECT id, body, created, author_id, post_id'
		' FROM comments'# http://www.runoob.com/sqlite/sqlite-joins.html
		' WHERE post_id = ?',
		(id,)#参数设置要注意格式 这里的 id 后一定要有, 
	).fetchall()
	return comments
```

关于 url\_for ，函数关于生成动态地址的用法https://blog.csdn.net/bestallen/article/details/52107944。
```python
return redirect(url_for('blog.view_post', id = id))
#此处的url_for 第二个参数应该直接按照对应端点（也就是视图函数）的参数设定去写。	
```

#### 7月21日
今天很成功，完成了点击帖子标题，显示一个帖子详细页面这个功能。

#### 7月20日
基本功能开发完毕，等待扩充功能。
今天把整个博客的基本功能实现完毕，还修复了几个 bug。
```python
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

```
> 上面只是为了测试一下代码高亮


第一个 bug 是当我在/create 里写完文章之后，页面的重定向发生错误，而且提示找不到模板。通过审视代码发现，模板文件夹设置没有错误，而且相对应的 index 模板本身也没有问题，从其他视图重定向进 index 视图函数是正常的，因此，问题被定位在 create 视图函数里。最后发现是重定向函数写成了返回模板函数
第二个 bug 是文章无法编辑，返回了一个奇葩错误。发现本该被传入的 `post` 是 `None`，回到视图函数，定位到`post = get_post(id)`这一行。id 定义本身没有问题，那问题被定位在`get_post`函数中，最后发现是没有写`return post`所致。