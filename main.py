from flask import request, redirect, render_template
#from flask_sqlalchemy import SQLAlchemy


from app import app, db
from models import User, Blog
from hashutils import make_pw_hash, check_pw_hash



@app.route('/newpost', methods=['POST','GET'])
def addpost():
    owner = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        title_name = request.form['title']
        blog_name = request.form['new_blog']
        title_error = ""
        blog_error = ""
       
        if title_name == "":
            title_error = "Please fill in the title"

        if blog_name == "":
            blog_error = "Please fill in the body"
         
        if not title_error and not blog_error:

            new_blog = Blog(title_name, blog_name, owner)
            db.session.add(new_blog)
            db.session.commit()  
            return redirect('/blog?id={}'.format(new_blog.id))
        
        else:
            return render_template('addpost.html', title_error=title_error,
            blog_error=blog_error)
    else:
        return render_template('addpost.html')
    



@app.route('/blog')
def mainblog():
    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts)
    else:
        post = Blog.query.get(blog_id)
        return render_template('indi_post.html', blog=post)
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password and check_pw_hash(password,user.pw_hash):
                session['user'] = user.username
                flash('welcome back, '+user.username)
                return redirect("/")
        flash('bad username or password')
        return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if ' ' in username:
            flash("You can't have space in your username")
            return redirect('/register')
        if username == '':
            flash("Please fill in username")
            return redirect('/register')
        
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken')
            return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/")
    else:
        return render_template('signup.html')


@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()


