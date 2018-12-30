import logging

class CommentCrawler(object):
    def __init__(self, praw_comment):
        self._stem_comment = praw_comment

    def get_stats(self):
        # word count, average word length, character count
        pass

    def get_wordcount(self):
        pass

    def get_ave_word_len(self):
        pass

    def get_char_count(self):
        pass

    def get_punctuation_count(self):
        pass

    def get_repeated_word_count(self):
        pass

    def get_shared_word_count(self, sub_comment):
        assert type(sub_comment) == type(self)
