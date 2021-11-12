# imports
import os
from flask import Flask   
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from database import db
from models import Post as Post
from models import User as User

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context

#@app.route('/')
@app.route('/index')
def index():
    a_user =  db.session.query(User).filter_by(email='cmoelle2@uncc.edu').one()
    return render_template("index.html", user = a_user)

@app.route('/posts')
def get_posts():
    a_user = db.session.query(User).filter_by(email='cmoelle2@uncc.edu').one()
    my_posts = db.session.query(post).all()

    return render_template('posts.html', posts=my_posts, user = a_user)

@app.route('/posts/<post_id>')
def get_post(post_id):
    a_user = db.session.query(User).filter_by(email='cmoelle2@uncc.edu').one()
    my_post = db.session.query(Post).filter_by(id=post_id).one()

    return render_template('post.html', post=my_post, user=a_user)

@app.route('/posts/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['postText']
        from datetime import date
        today = date.today()
        today = today.strftime("%m-%d-%Y")
        new_record = Post(title, text, today)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('get_posts'))
    else:
        a_user = db.session.query(User).filter_by(email='cmoelle2@uncc.edu').one()
        return render_template('newpost.html', user=a_user)


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)