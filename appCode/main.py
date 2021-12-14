import os
import bcrypt
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from database import db_init, db
from models import Post as Post
from models import User as User
from models import Img as Img
from flask import session
import datetime
from forms import RegisterForm
from forms import LoginForm
from models import Comment as Comment
from forms import CommentForm
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template("index.html", user=session['user'])
    return render_template("index.html")


@app.route('/posts')
def get_posts():
    if session.get('user'):
        my_posts = db.session.query(Post).filter_by(user_id=session['user_id']).all()
        return render_template('posts.html', posts=my_posts, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/allposts')
def get_allposts():
    all_posts = db.session.query(Post).all()
    return render_template('allposts.html', posts=all_posts, user=session['user'])


@app.route('/posts/<post_id>')
def get_post(post_id):
    if session.get('user'):
        my_post = db.session.query(Post).filter_by(id=post_id).one()
        form = CommentForm()
        return render_template('post.html', post=my_post, user=session['user'], form=form)
    else:
        return redirect(url_for('login'))


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['postText']
            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Post(title, text, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('get_posts'))
        else:
            return render_template('new.html', user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/posts/edit/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['postText']
            post = db.session.query(Post).filter_by(id=post_id).one()
            post.title = title
            post.text = text
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('get_posts'))
        else:
            my_post = db.session.query(Post).filter_by(id=post_id).one()
            return render_template('new.html', post=my_post, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/posts/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    if session.get('user'):
        my_post = db.session.query(Post).filter_by(id=post_id).one()
        db.session.delete(my_post)
        db.session.commit()
        return redirect(url_for('get_posts'))
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_user = User(first_name, last_name, request.form['email'], h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = first_name
        session['user_id'] = new_user.id
        return redirect(url_for('get_posts'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            return redirect(url_for('get_posts'))
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


@app.route('/posts/<post_id>/comment', methods=['POST'])
def new_comment(post_id):
    if session.get('user'):
        comment_form = CommentForm()
        if comment_form.validate_on_submit():
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(post_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()
        return redirect(url_for('get_post', post_id=post_id))
    else:
        return redirect(url_for('login'))


@app.route('/upload', methods=['POST'])
def upload():
    pictures = request.files['/Pictures/']
    if not pictures:
        return 'No picture uploaded!', 400
    filename = secure_filename(pictures.filename)
    mimetype = pictures.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400
    img = Img(img=pictures.read(), name=filename, mimetype=mimetype, post_id=post_id, user_id=user_id)
    db.session.add(img)
    db.session.commit()

    return 'Img Uploaded!', 200


@app.route('/upload/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.img, mimetype=img.mimetype)


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000
