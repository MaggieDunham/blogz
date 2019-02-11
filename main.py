from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
   

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/add-new-post', methods=['POST', 'GET'])
def add_new_post():

    if request.method == 'POST':
        title_name = request.form['titlename']
        post_name = request.form['contribution']
        new_blog = Blog(title_name, post_name)
        title_error = ''
        contribution_error = ''
        if title_name == '':
            title_error = "Please name your Blog"

        if post_name == '':
            contribution_error = "Please make a blog"
            return render_template('add-new-post.html', title_error=title_error, contribution_error=contribution_error)
        else:    
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_blog.id))

    return render_template('add-new-post.html')


@app.route('/blog', methods=['GET'])
def blog():

    blogpost = request.args.get('id')
    if blogpost is not None:
        blogs = Blog.query.filter_by(id=blogpost)
        return render_template('blog-list.html', blogs=blogs)

    else:
        blogs = Blog.query.all()

        return render_template('blog.html', blogs=blogs)

if __name__ == '__main__':
    app.run()