from database import db
import datetime


class Post(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    likes = db.Column("likes", db.Integer)
    comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)

    def __init__(self, title, text, date, user_id, likes):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = user_id
        self.likes = likes


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    posts = db.relationship("Post", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, post_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.post_id = post_id
        self.user_id = user_id

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column("userID", db.Integer)
    darkModeToggle = db.Column("darkModeToggle", db.Integer)

    def __init__(self, userID, darkModeToggle):
        self.userID = userID
        self.darkModeToggle = darkModeToggle

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, img, name, mimetype, post_id, user_id):
        self.img = img
        self.name = name
        self.mimetype = mimetype
        self.post_id = post_id
        self.user_id = user_id
