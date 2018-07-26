from flask import Flask, render_template, request,  send_from_directory
from model import Article, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from mailwatch import generate_slug, generate_slug_without_title
from sqlalchemy.pool import SingletonThreadPool
import os 

app = Flask(__name__)

engine = create_engine('sqlite:///articles.db', poolclass=SingletonThreadPool   )
Base.metadata.bind = engine

session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)


@app.route('/')
def hello_world():
    return render_template('home.html')


# Serve static files from the respective directories

@app.route('/article_files/<path:path>')
def send_js(path):
    return send_from_directory('article_files', path)

@app.route('/content_files/<path:path>')
def send1_js(path):
    return send_from_directory('content_files', path)

@app.route('/index_files/<path:path>')
def send2_js(path):
    return send_from_directory('index_files', path)


@app.route('/assets/<path:path>')
def send3_js(path):
    return send_from_directory('assets', path)

@app.route('/assets/js/<path:path>')
def send5_js(path):
    return send_from_directory('assets/js', path)

@app.route('/assets/css/<path:path>')
def send6_js(path):
    return send_from_directory('assets/css', path)

@app.route('/images/<path:path>')
def send4_js(path):
    return send_from_directory('images', path)

# Display single post

@app.route('/<alias>/<urlslug>')
def show_user_profile(alias,urlslug):
    print(urlslug)
    # show the user profile for that user
    db_search = session.query(Article).filter(
                Article.alias == alias,
                Article.urlslug == urlslug
            ).first()
    return render_template('content.html', alias = alias, article=db_search)

# Display all posts of an alias
@app.route('/<alias>')
def get_all_posts(alias):
    # show the user profile for that user
    db_search = session.query(Article).filter(
                Article.alias == str(alias),
            ).all()
    return render_template('index.html', alias = alias, articles=db_search)

# For debug only
@app.route('/all')
def get_all():
    # show the user profile for that user
    db_search = session.query(Article).filter(
                Article.alias is not None,
            ).all()
    strg = ""
    for article in db_search:
        strg += "<h1>"+article.title+"</h1>"
        strg += "<h4>"+article.urlslug+"</h4>"
        strg += "<br><br>"
    return strg

# For debug and demo purposes only
@app.route('/deleteall')
def delete_all():
    # show the user profile for that user
    db_search = session.query(Article).delete()
    session.commit()
    return "Number deleted : "+str(db_search)