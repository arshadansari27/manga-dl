from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('sqlite:///manga.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    xml = Column(String)
    chapters = relationship("Chapter", backref=backref("feed", order_by=id))

    def __init__(self, name, link, xml):
        self.name = name
        self.link = link
        self.xml = xml


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    done = Column(Boolean)
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    pages = relationship("Page", backref=backref("chapter", order_by=title))

    def __init__(self, title, link, feed):
        self.title = title
        self.link = link
        self.done = False
        self.feed_id = feed.id

    def __lt__(self, other):
        return self.title < other.title

    def __gt__(self, other):
        return self.title > other.title


class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    page_link = Column(String)
    image_link = Column(String)
    next_page_id = Column(Integer, ForeignKey("pages.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    downloaded = Column(Boolean)

    def __init__(self, link, chapter):
        self.page_link = link
        self.chapter_id = chapter.id
        self.downloaded = False

    def __repr__(self):
        return str(self.id) + ": " + self.link + ", " + self.image_link

    def __lt__(self, other):
        return self.page_link < other.page_link

    def __gt__(self, other):
        return self.page_link > other.page_link


Base.metadata.create_all(engine)
