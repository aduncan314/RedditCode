import re

from collections import OrderedDict

class CommentCalculator(object):
    def __init__(self, comment_text):
        self.full_comment_text = comment_text
        self._word_list = re.findall('\w+', self.full_comment_text)

    def get_all_stats(self):
        # word count, average word length, character count
        all_stats_dict = {
            'wordcount': self.get_wordcount(),
            'ave_len': self.get_ave_word_len(),
            'char_count': self.get_char_count(),
            'punctuation_count': self.get_punctuation_count()
        }
        return all_stats_dict

    def get_wordcount(self):
        return len(self._word_list)

    def get_ave_word_len(self):
        length_sum = float(sum([len(word) for word in self._word_list]))
        return length_sum / self.get_wordcount()

    def get_char_count(self):
        return len(self.full_comment_text.strip())

    def get_punctuation_count(self, distinct_sets=True):
        if distinct_sets:
            all_punct = re.findall('[^\w\s]+', self.full_comment_text) # TODO: double check regex!!
        else:
            all_punct = re.findall('[^\w\s]', self.full_comment_text)

        return len(all_punct)

    def get_repeated_word_count(self):
        all_words_dict = {}

        for word in self._word_list:
            try:
                all_words_dict[word] += 1
            except KeyError:
                all_words_dict[word] = 1

        return OrderedDict(sorted(all_words_dict.items(), key=lambda x: x[1], reverse=True))

    def get_shared_word_count(self, sub_comment_text):
        return len(self.get_shared_word(sub_comment_text))

    def get_shared_word(self, sub_comment_text):
        sub_comment_calc = CommentCalculator(sub_comment_text)
        sub_counts = sub_comment_calc.get_repeated_word_count()

        coincident_count = []
        for word in self.get_repeated_word_count().keys():
            if word in sub_counts.keys():
                coincident_count.append(word)

        return coincident_count

    def get_shared_word_ratio(self, sub_comment_text):
        """
        Return dictionary with ratio of parent/child word count ratio for all repeated words
        :param sub_comment_text:
        :return:
        """
        sub_comment_calc = CommentCalculator(sub_comment_text)
        sub_repeated_word_count = sub_comment_calc.get_repeated_word_count()
        stem_repeated_word_count = self.get_repeated_word_count()

        shared_words = self.get_shared_word(sub_comment_text)
        ratio_dict = {}

        for word in shared_words:
            ratio_dict[word] = float(stem_repeated_word_count[word]) / float(sub_repeated_word_count[word])

        return OrderedDict(sorted(ratio_dict.items(), key=lambda x: x[1], reverse=True))

    def __str__(self):
        return self.full_comment_text

    def __len__(self):
        return len(self.full_comment_text)