#!/bin/env python3

from post import Post
import datetime
import time

class DBService:
    def __init__(self):
        pass

    def get_last_date(self):
        # Query database and get time
        return datetime.datetime.fromtimestamp(
            time.time() - 100000
        )

    def write(self, p):
        pass
