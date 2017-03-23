#!/bin/env python3
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, BigInteger, String, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from config import postgres

Base = declarative_base()

class Post(Base):
    '''
    Model for a facebook Post
    '''
    __tablename__ = 'posts'

    post_id = Column(BigInteger, primary_key=True)
    author = Column(String)
    time = Column(Time)
    content = Column(String)
    date = Column(Date)
    posting_date = Column(DateTime)
    to = Column(String)
    frm = Column(String)
    def __init__(self, posting_date, author, content, post_id):
        '''
        Initialize Post with posting_date, author and content
        '''
        self.date = None
        self.author = author
        self.content = content
        self.to = None
        self.frm = None
        self.posting_date = posting_date
        self.time = None
        self.post_id = int(post_id)

    def __str__(self):
        '''
        Method for pretty printing
        '''
        return '\n'.join(['Content: ' + str(self.content),
                          'Author: ' + str(self.author),
                          'Posting Date: ' + str(self.posting_date),
                          'To: ' + str(self.to),
                          'From: ' + str(self.frm),
                          'Time: ' + str(self.time),
                          'Date: ' + str(self.date),
                          'PostId: ' + str(self.post_id)
                          ])

if __name__ == '__main__':
    engine = create_engine(''.join(['postgresql://',
                                    postgres['USERNAME'], ':',
                                    postgres['PASSWORD'], '@',
                                    postgres['HOST'], '/',
                                    postgres['DB']]),
                           echo = False)
    Base.metadata.create_all(engine)
