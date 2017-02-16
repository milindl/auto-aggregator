#!/bin/env python3

import facebook
from db_service import DBService
from post import Post
import datetime

# Config?
GROUP_ID = '433290100027449'

class Aggregator:
    def __init__(self, access_token):
        self.graph = facebook.GraphAPI(access_token = access_token,
                                       version = '2.3')

    def update(self, dbs):
        since = dbs.get_last_date().strftime('%Y-%m-%d %H:%M:%S')
        posts_dict = self.graph.get_object(
            id = GROUP_ID + '?fields=feed.since(' + since + ')'
        )
        posts = []
        for p in posts_dict['feed']['data']:
            posts.append(Post(
                date = datetime.datetime.strptime(p['created_time'],
                                                  '%Y-%m-%dT%H:%M:%S%z'),
                author = p['from']['name'],
                content = p['message'],
                post_id = p['id'].split('_')[1]
            ))
        final_posts = [ self.process(p) for p in posts ]
        dbs.write(final_posts)

    def process(self, post):
        # Process post thru self.PostReader
        # Return processed post
        return post




if __name__ == '__main__':
    Aggregator(
        'EAACEdEose0cBAFMGYgl6hg48mwv0Xm4nChngZB6DRz6yR0eQZARZCOOJbuticJxToc4eHVvx88XG6oAWaZBJ0EW4GsehjTZCNoeZBhC3gK80Ir1qnUSwvYirbMZBYOE8nMs2uSbZA6NYkxqrSMS1dLvme8Tp6YW7sgyQWEkhXLZCuJJ4vAIjQKf4Rkpyh0wfDoxMZD'
    ).update(DBService())
