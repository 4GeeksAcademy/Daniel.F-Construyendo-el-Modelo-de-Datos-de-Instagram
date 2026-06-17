from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts: Mapped[list["Post"]] = relationship("Post")
    comments: Mapped[list["Comment"]] = relationship("Comment")
    following: Mapped[list["Follower"]] = relationship(
        "Follower", foreign_keys="Follower.user_from_id")
    followers: Mapped[list["Follower"]] = relationship(
        "Follower",  foreign_keys="Follower.user_to_id")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User")
    media: Mapped[list["Media"]] = relationship("Media")
    comments: Mapped[list["Comment"]] = relationship("Comment")

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship("Post")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    author: Mapped["User"] = relationship("User")
    post: Mapped["Post"] = relationship("Post")

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    user_from: Mapped["User"] = relationship(
        "User", foreign_keys=[user_from_id])
    user_to: Mapped["User"] = relationship("User", foreign_keys=[user_to_id])