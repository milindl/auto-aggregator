#!/bin/env python3

class Post: # pylint: disable=too-few-public-methods
    '''
    Model for a facebook Post
    '''
    def __init__(self, posting_date, author, content, post_id):
        '''
        Initialize Post with posting_date, author and content

        Example usage:
        Post(datetime.date.today(), 'Milind', content: 'abc', post_id)
        '''
        self.date = None
        self.author = author
        self.content = content
        self.to = None
        self.frm = None
        self.posting_date = posting_date
        self.time = None

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
                          'Date: ' + str(self.date)])
