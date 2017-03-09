#!/bin/env python3

import facebook
from db_service import DBService
from post import Post
import post_reader
import datetime
from config import graph_api


class Aggregator:
    def __init__(self, access_token):
        self.graph = facebook.GraphAPI(access_token = access_token,
                                       version = '2.3')
        self.pread = post_reader.PostReader()

    def update(self, dbs):
        since = str(dbs.get_last_date())
        posts_dict = self.graph.get_object(
            id = f'{graph_api["GROUP_ID"]}?fields=feed.since({since})'
        )
        posts = []
        for p in posts_dict['feed']['data']:
            posts.append(Post(
                posting_date = datetime.datetime.strptime(p['created_time'],
                                                  '%Y-%m-%dT%H:%M:%S%z'),
                author = p['from']['name'],
                content = p['message'],
                post_id = p['id'].split('_')[1]
            ))
        final_posts = []
        for p in posts:
            try:
                final_posts.append(self.process(p))
            except Exception:
                print('Could not log a post')
                final_posts.append(p)
                continue
        dbs.write(final_posts)

    def process(self, post):
        # Process post thru self.PostReader
        # Return processed post
        post = self.pread.read_post(post)
        print(post)
        print('#########')
        return post


def Main():
    Aggregator(graph_api['TOKEN']).update(DBService())

if __name__ == '__main__':
    Main()
