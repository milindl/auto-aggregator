#!/bin/env python3

class Post: # pylint: disable=too-few-public-methods
    '''
    Model for a facebook Post
    '''
    def __init__(self, date, author, content, post_id):
        '''
        Initialize Post with date, author and content
        Content is a dictionary

        Example usage:
        Post(datetime.date.today(), 'Yash Srivastav', { content: 'abc' })
        '''
        self.date = date
        self.author = author
        self.content = content
