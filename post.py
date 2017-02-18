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
        self.date = None
        self.author = author
        self.content = content
        self.to = None
        self.frm = None
        self.posting_date = date
        self.time = None

    def __str__(self):
        return '\n'.join(['Content: ' + str(self.content),
                          'Author: ' + str(self.author),
                          'Posting Date: ' + str(self.posting_date),
                          'To: ' + str(self.to),
                          'From: ' + str(self.frm),
                          'Time: ' + str(self.time),
                          'Date: ' + str(self.date)])
