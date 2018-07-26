from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
class Article(Base):
     __tablename__ = 'article'

     id = Column(Integer, primary_key=True)
     title = Column(String,nullable=False)
     name = Column(String,nullable=False)
     body = Column(Text)
     alias = Column(String,nullable=False)
     time = Column(DateTime,nullable=False)     
     urlslug = Column(String,nullable=False)

     def __repr__(self):
        return "<%s> by %s" % (
                             self.title, self.alias)

engine = create_engine('sqlite:///articles.db')
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)


