#!/bin/env python3

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from post import Post
import datetime
import time
import sqlalchemy
from config import postgres


INDIAN_TIMEZONE_SHIFT = 19800

class DBService:
    def __init__(self):
        self.engine = create_engine(''.join(['postgresql://',
                                             postgres['USERNAME'], ':',
                                             postgres['PASSWORD'], '@',
                                             postgres['HOST'], '/',
                                             postgres['DB']]),
                                    echo = False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_last_date(self):
        '''
        Query database and get time of last parsed post
        '''
        # Update as per latest post time
        try:
            latest_post = self.session.query(Post).order_by(Post.posting_date)[-1]
            print('Latest post: ' + str(latest_post))
            return latest_post.posting_date.timestamp() + INDIAN_TIMEZONE_SHIFT
        except IndexError:
            return '01/01/2017'
        # Check on an hourly basis
        # Hourly check: the db may be updated thru our app also
        # return '-1 hour'

    def write(self, p):
        for pst in p:
            self.session.merge(pst)
        # TODO: Make this better in terms of efficiency
        self.session.commit()
