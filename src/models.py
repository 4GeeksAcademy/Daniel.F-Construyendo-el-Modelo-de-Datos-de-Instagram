import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
import datetime

Base = declarative_base()

# 1. TABLA DE USUARIOS
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    biography = Column(Text, nullable=True)

    # Relaciones: Un usuario puede tener muchos posts y comentarios
    posts = relationship('Post', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

# 2. TABLA DE PUBLICACIONES (POSTS)
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False) # Link de la foto en Instagram
    caption = Column(Text, nullable=True)            # El pie de foto / descripción
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Llave foránea: Vincula el Post con el Usuario que lo creó
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Relación: Un post puede tener muchos comentarios
    comments = relationship('Comment', backref='post', lazy=True)

# 3. TABLA DE COMENTARIOS
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Llaves foráneas: ¿Quién comentó y en qué Post comentó?
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

# 4. TABLA DE SEGUIDORES (FOLLOWER) - Relación de muchos a muchos
class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    
    # El usuario que sigue a otra persona
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # El usuario que es seguido por otra persona
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)


## Generar el diagrama automáticamente (No borres esto si ya viene en el archivo)
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! El archivo diagram.png ha sido actualizado.")
except Exception as e:
    print("Hubo un problema generando el diagrama")
    raise e