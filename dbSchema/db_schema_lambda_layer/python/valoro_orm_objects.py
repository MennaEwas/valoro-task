from typing_extensions import Required
from pkg_resources import require
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import FLOAT

Base = declarative_base()


def create_db_schema(engine):
    Base.metadata.create_all(engine)


class Group(Base):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement= True)
    name = Column(String(255), nullable= True)
    groupTypeId = Column(Integer, nullable=True)
    img = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=True)
    cost = Column(FLOAT, nullable=True)
    description = Column(String(255), nullable= True, default= "Description for the group")


    def __repr__(self):
        return "<Group(name='%s', img='%s', capacity='%d', description='%s', cost='%f')>" % (
            self.name, self.img, self.capacity, self.description, self.cost)

    def __init__(self, name = None, img = None, groupTypeId=None, capacity=None, description=None):
        self.name = name
        self.img = img
        self.groupTypeId = groupTypeId
        self.capacity = capacity
        self.description = description

class Reply(Base):
    __tablename__ = 'reply'

    id = Column(Integer, primary_key=True, autoincrement=True)
    replyTitle = Column(String(255), nullable=False)
    replyComment = Column(String(255), nullable=True)
    voiceNoteLink = Column(String(255), nullable=True)

    def __repr__(self):
        return "<Reply(replyTitle='%s', replyComment='%s', voiceNoteLink='%s'')>" % (
            self.replyTitle, self.replyComment, self.voiceNoteLink)

    def __init__(self, replyTitle, replyComment=None, voiceNoteLink=None):
        self.replyTitle = replyTitle
        self.replyComment = replyComment
        self.voiceNoteLink = voiceNoteLink
