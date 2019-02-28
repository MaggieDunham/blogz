from flask import Flask, request, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'lostgirl'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    

    def __init__(self, owner, title, body):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.Column(db.String(1200))
   

    def __init__(self, username, password):
        self.username = username
        self.password = password
             



@app.route('/addnewpost', methods=['POST', 'GET'])
def addnewpost():

    if request.method == 'POST':
        title_name = request.form['titlename']
        post_name = request.form['contribution']
        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(owner, title_name, post_name)
        title_error = ''
        contribution_error = ''
        if title_name == '':
            title_error = "Please name your Blog"

        if post_name == '':
            contribution_error = "Please make a blog"
            return render_template('addnewpost.html', title_error=title_error, contribution_error=contribution_error)
        else:    
            db.session.add(new_blog)

            db.session.commit()
            return redirect('/blog?id={0}'.format(new_blog.id))

    return render_template('addnewpost.html')
@app.route('/')
def index():
    users = User.query.all()    
    return render_template('index.html',users=users)

@app.route('/blog', methods=['GET','POST'])
def blog():

    blogpost = request.args.get('id')
    if blogpost is not None:
        blogs = Blog.query.filter_by(id=blogpost)
        return render_template('addnewpost.html', blogs=blogs)

    elif request.args.get('user'):
        userID = request.args.get('user')
        blogs = Blog.query.filter_by(owner_id=userId).all()
        return render_template('singleuser.html', blogs=blogs)

    else:
        blogs = Blog.query.all()

        return render_template('blog.html', blogs=blogs)

#@app.route('/signup')
#def signup():
 #   return render_template('signup.html')
def empty_val(x):
    if x == "":
        return True
    else:
        return False

def char_length(x):
    if len(x) > 2 and len(x) < 21:
        return True
    else:
        return False
def email_symbol(x):
    if x.count('@') >= 1:
        return True
    else:
        return False
def email_symbol_plus_one(x):
    if x.count('@') <= 1:
        return True
    else:
        return False
def email_period(x):
    if x.count('.') >=1:
        return True
    else:
        return False
def email_period_plus_one(x):
    if x.count('.') <=1:
        return True
    else:
        return False

#this creates the route to validate 

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        #validate user's data
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/addnewpost')
        else:
            # flash message you already exist
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')


#this creates varibles from the inputs

    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify']
    email = request.form['email']

#this creates empty strings for error messages

    username_error = ""
    password_error = ""
    verify_password_error = ""
    email_error = ""

#these are the error messages

    err_required = "Required field"
    err_reenter_pw = "Please re-enter password"
    err_char_count = "must be between 3 and 20 characters"
    err_no_spaces = "must not contain spaces"

#this is password verification

    if empty_val(password):
        password_error = err_required
        password = ''
        verify_password = ''
    elif not char_length(password):
        password_error = "Password " + err_char_count
        password = ''
        verify_password = ''
    else:
        if " " in password:
            password_error = "Password " + err_no_spaces
            password = ''
            verify_password = ''

#this is the second password verification

    if empty_val(verify_password):
        verify_password_error = err_required
        password = ''
        verify_password = ''
    elif not char_length(verify_password):
        verify_password_error = "Password " + err_char_count
        password = ''
        verify_password = ''
    elif " " in verify_password:
        verify_password_error = "Password " + err_no_spaces
        password = ''
        verify_password = ''
    else:
        if verify_password != password:
            verify_password_error = "Passwords must match"
            password = ''
            verify_password = ''

#this is username verification            

    if empty_val(username):
        username_error = err_required
        password = ''
        verify_password = ''
    elif not char_length(username):
        username_error = "Username " + err_char_count
        password = ''
        verify_password = ''    
    else:
        if " " in username:
            username_error = "Username " + err_no_spaces
            password = ''
            verify_password = ''

#this is the email verification            


    if not char_length(email):
        email_error = "Email " + err_char_count
        password = ''
        verify_password = ''
    elif not email_symbol(email):
        email_error = "Email must contain the @ symbol"
        password = ''
        verify_password = ''
    elif not email_symbol_plus_one(email):
        email_error = "Email must contain only one @ symbol"
        password = ''
        verify_password = ''
    elif not email_period(email):
        email_error = "Email must contain ."
        password = ''
        verify_password = ''
    elif not email_period_plus_one(email):
        email_error = "Email must contain only one ."
        password = ''
        verify_password = ''
    else:
        if " " in email:
            email_error = "Email " + err_no_spaces
            password = ''
            verify_password = ''

    if email == "": 
        email_error = ""

    if not username_error and not password_error and not verify_password_error and not email_error:
        new_user= User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['user']=new_user.id
        return redirect('/blog')
    else:
        return render_template('signup.html', username_error=username_error, username=username, 
        password_error=password_error, password=password, verify_password_error=verify_password_error,
         verify_password=verify_password, email_error=email_error, email=email)
#now run it 

@app.before_request   
def require_login():
    allowed_routes = ['login', 'blog', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST','GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = user.username 
            return redirect('/addnewpost')          
        username_error=''
         # add session
        if not user:
            username_error="Incorrect Username"
        return render_template('login.html', username_error=username_error)
        #flash error

    return render_template('login.html')



@app.route('/logout', methods=['POST','GET'])
def logout():
    del session['user']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()