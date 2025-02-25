from sqlalchemy import Column, Integer, String
from models.base import Base

class User(Base):
    __name__ = "users"


