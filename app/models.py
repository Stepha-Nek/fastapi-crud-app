from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  # Importing necessary SQLAlchemy components to define the database schema
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship  # Importing relationship to define relationships between tables

class Post(Base):
    __tablename__ = "posts"  # This is the name of the table in the database.

    id = Column(Integer, primary_key=True, nullable=False) # This is the primary key for the table.
    title = Column(String, nullable=False)  # This is a column in the table.
    content = Column(String, nullable=False)  # This is another column in the table.
    published = Column(Boolean, server_default = 'TRUE', nullable=False)  # This is a boolean column in the table, its the sql server that will default or set constraints thats y its written like that
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  # This is a timestamp column in the table, it will be set to the current time when a new row is created.
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # This is a foreign key column in the table, it will be used to link the post to the user that created it, it cannot be null because every post must have an owner.
    owner = relationship("User")  # This will create a relationship between the Post and User models, allowing you to access the user that created the post using post.owner.

#model for user, this is the user that will be created when a new user registers, it inherits from Base which is the base class for all models in the database.
#this is the table created in the database when user registers, we still need a model so only the information we need is given by user
class User(Base):
    __tablename__ = "users"  # This is the name of the table in the database.

    id = Column(Integer, primary_key=True, nullable=False)  # This is the primary key for the table.
    email = Column(String, nullable=False, unique=True)  # This is a column in the table, it has to be unique., one account with one email, cant register twice
    password = Column(String, nullable=False)  # This is another column in the table.
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  # This is a timestamp column in the table.
    #nullable , False means that this column cannot be null, it has to have a value when a new row is created.

    Base = Base  # 👈 explicitly expose Base so models.Base works

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  # This is a foreign key column in the table, it will be used to link the vote to the user that created it, it cannot be null because every vote must have an owner.
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)  # This is a foreign key column in the table, it will be used to link the vote to the post that was voted on, it cannot be null because every vote must be linked to a post.
