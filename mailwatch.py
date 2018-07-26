import win32com.client
import time
from model import Article, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import dateutil.parser


datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

inbox = outlook.GetDefaultFolder(6)
 
engine = create_engine('sqlite:///articles.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

def generate_slug(s):
    allowed = "abcdefghijklmnopqrstuvwxyz1234567890 "
    s = str.lower(s)
    tagless = s.split("[article]")[1].strip()
    result = ""
    for word in tagless:
        if word == " " or word == "|" or word == "/":
            word = "-"
        if word not in allowed: 
            continue
        result += word
    return result[:35]

def generate_slug_without_title(s):
    allowed = "abcdefghijklmnopqrstuvwxyz1234567890 "
    s = str.lower(s)
    result = ""
    for word in s:
        if word == " " or word == "|" or word == "/":
            word = "-"
        if word not in allowed: 
            continue
        result += word
    return result[:35]

def get_alias(s):
    return s.split("@")[0]

def watcher():
    try:
        # Check for email every 10 seconds. 
        print(">> Listening for new emails")
        messages = inbox.Items
        message = messages.GetLast()
        if "[article]" in str.lower(message.subject):
            # Article is found

            # Check if the article is pre-existing 

            db_search = session.query(Article).filter(
                Article.name == str(message.Sender),
                Article.urlslug == generate_slug(message.subject)
            ).first()
            if db_search is not None:
                print("   - Found existing article")
            else:
                sub = str.lower(message.subject)
                new_article = Article(
                    title= sub.split("[article]")[1].strip(),
                    name = str(message.Sender),   
                    body = message.HTMLBody,
                    alias = get_alias(message.Sender.GetExchangeUser().PrimarySmtpAddress),
                    time = dateutil.parser.parse(str(message.SentOn)),
                    urlslug = generate_slug(message.subject)
                    )
                session.add(new_article)
                session.commit()
            
        time.sleep(10)
    except Exception as e:
        print(e)
        time.sleep(10)

if __name__ == "__main__":
    while True:
        watcher()
    