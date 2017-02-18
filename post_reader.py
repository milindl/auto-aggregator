#!/bin/env python3

from post import Post
import datetime
from fuzzywuzzy import fuzz
import re
import dateutil.parser as dp
import parsedatetime as pdt
import calendar

class PostReader:
    '''
    Class to parse posts and populate them with information
    '''
    def __init__(self, mapping_file = 'mappings', stoplist = set()):
        '''
        Initialize PostReader with mappings etc
        mapping_file can be used to provide a file for location -> keyword maps
        Example mapping_file:
        location1;keyword1,key phrase,key phrase two
        location2;key phrase three,keyword2,keyword3

        stoplist is the set()  of words not to include in token tuples
        '''
        if len(stoplist) == 0:
            self.stoplist = set('in on at to from or around'.split())
        else:
            self.stoplist = stoplist
        loc_file = open(mapping_file)
        loc_map = {}
        for line in loc_file:
            ans = line.split(';')[0]
            for key in line.split(';')[1].replace('\n', '').split(','):
                loc_map[key] = ans
        self.loc_map = loc_map

    def loc_tokenizer(self, preceding_word, suceeding_word, pst):
        '''
        Returns a tuple containing possible location strings in mes
        Finds 2 words after the preceding_word and eliminates any stoplist words
        '''
        preceding_word = re.sub('([a-zA-Z]+)', '\g<1> ', preceding_word)
        suceeding_word = re.sub('([a-zA-Z]+)', ' \g<1>', suceeding_word)
        m = re.search(preceding_word +
                      '([a-zA-Z]+)? ([a-zA-Z]+)?' +
                      suceeding_word,
                       pst.content) or re.search(preceding_word +
                                                 '([a-zA-Z]+)?' +
                                                 suceeding_word,
                                                 pst.content)
        if not m:
            return ()
        final = []
        for g in m.groups():
            if g.lower() not in self.stoplist: final.append(g.lower())

        return tuple(final)

    def best_scoring_value(self, groups):
        '''
        Finds best fuzzy match
        Compares each elem of the group with each keyphrase/word in loc_map
        Returns the location with best matching
        '''
        best_match = ''
        best_score = 0
        groups = list(groups)
        groups.append(' '.join(groups))
        for g in groups:
            for key in self.loc_map:
                if fuzz.ratio(key, g) > best_score:
                    best_score = fuzz.ratio(key, g)
                    best_match = self.loc_map[key]
        return best_match

    def get_temporal(self, pst):
        cal = pdt.Calendar()
        # Space out all punctuation from post content
        # This seems to improve guessing
        content = re.sub('([^a-zA-Z0-9\:\-\+])', ' \g<1> ', pst.content)
        content = re.sub('[ ]+', ' ', content)
        naked_content = re.search('([0-3]?[0-9])[ ]?(st|nd|rd|th)? (?!Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|am|pm|A\.M\.|P\.M\.)',
                                  content, re.I)
        if naked_content:
            # Assumption: only one such naked date exists
            d = int(naked_content.groups()[0])
            month_name = ''
            if d >= pst.posting_date.day:
                month_name = calendar.month_name[pst.posting_date.month]
            else:
                month_name = calendar.month_name[(pst.posting_date.month % 12) + 1]
            content = re.sub('([0-3]?[0-9])[ ]?(st|nd|rd|th)? (?!Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|am|pm|A\.M\.|P\.M\.|noon)[A-Za-z]+',
                             '\g<0>' + month_name + ' ', content, re.I)
        nlp_guess = cal.nlp(content, sourceTime = pst.posting_date)
        if len(nlp_guess) == 0:
            return None

        # In case we have only one parse, get to to caller
        if len(nlp_guess) == 1:
            return (nlp_guess[0][0],)
        # In case we have >= 2 parses, need to separate them into Time and Date
        time_parsed = []
        date_parsed = []
        weird_parsed = []  # Strings which fail dateutil.parser.parse
        for guess in nlp_guess:
            try:
                if dp.parse(guess[-1]).time() == dp.parse('00:00').time():
                    date_parsed.append(guess)
                else:
                    time_parsed.append(guess)
            except ValueError:
                weird_parsed.append(guess)
        if len(time_parsed) > 0 and len(date_parsed) > 0:
            return (dp.parse(time_parsed[-1][-1]), dp.parse(date_parsed[0][-1]))
        elif len(date_parsed) > 0:
            return (dp.parse(date_parsed[0][-1]),)
        else:
            return (weird_parsed[0][0],)

    def read_post(self, p):
        '''
        Method to read a raw post and extract relavant content from it
        '''
        to_groups = self.loc_tokenizer('to', '', p) or self.loc_tokenizer('for', '', p)
        best_to = self.best_scoring_value(to_groups)
        from_groups = self.loc_tokenizer('from', '', p) or self.loc_tokenizer('', 'to', p)
        best_from = self.best_scoring_value(from_groups)
        p.to = best_to
        p.frm = best_from
        dates = self.get_temporal(p)
        if len(dates) == 1:
            p.date = dates[0].date()
            p.time = dates[0].time()
        else:
            p.date = dates[1].date()
            p.time = dates[0].time()
        return p
