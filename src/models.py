import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    firstname: Mapped[str] = mapped_column(String(250), nullable=False)
    lastname: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False)

    posts = relationship("Post", back_populates="post_user")
    comments = relationship("Comment", back_populates="comment_author")
    followers = relationship("Follower", foreign_keys="Follower.user_from_id", back_populates="follower_from")
    following = relationship("Follower", foreign_keys="Follower.user_to_id", back_populates="follower_to")

class Follower(Base):
    __tablename__ = 'follower'
    
    user_from_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)

    follower_from = relationship("User", foreign_keys=[user_from_id], back_populates="followers")
    follower_to = relationship("User", foreign_keys=[user_to_id], back_populates="following")

class Post(Base):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    post_user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="media_post")
    comments = relationship("Comment", back_populates="comment_post")

class Media(Base):
    __tablename__ = 'media'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)

    media_post = relationship("Post", back_populates="media")

class Comment(Base):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)

    comment_author = relationship("User", back_populates="comments")
    comment_post = relationship("Post", back_populates="comments")
    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
