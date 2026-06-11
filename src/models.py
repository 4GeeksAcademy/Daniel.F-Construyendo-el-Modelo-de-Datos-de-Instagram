import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    biography = Column(Text)

    posts = relationship('Post', backref='user')
    comments = relationship('Comment', backref='user')
    likes = relationship('Like', backref='user')


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    comments = relationship('Comment', backref='post')
    likes = relationship('Like', backref='post')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)


class Follower(Base):
    __tablename__ = 'follower'

    id = Column(Integer, primary_key=True)

    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)


try:
    render_er(Base, 'diagram.png')
    print("¡Éxito! El archivo diagram.png ha sido actualizado.")
except Exception as e:
    print("Hubo un problema generando el diagrama")
    raise e