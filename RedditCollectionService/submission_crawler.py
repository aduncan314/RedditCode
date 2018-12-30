import warnings
import logging

from RedditCollectionService.reddit_connection_maker import connection_factory
from RedditCollectionService.comment_calculator import CommentCalculator


class SubmissionCrawler(object):
    """
    Returns data relating adjacent comment levels for the first acceptable submission.

    DEFINE ACCEPTABLE SUBMISSION
    """

    def __init__(self, subreddit):
        self._subreddit_name = subreddit
        self.read_only_reddit = connection_factory('read_only')
        self.sub = self.read_only_reddit.subreddit(self._subreddit_name)

        self.comment_ordering = 'hot'

        self._MAX_NUM_TOP_LEVEL_COMMENTS = 10
        self._MAX_SUBMISSIONS_SEARCH = 30

        self._depth = 0

        logging.info("Getting comments for {}".format(self._subreddit_name))
        self._submission = self._get_acceptable_submission()
        self._submission_title = self._submission.title

    def __str__(self):
        return "SubmissionCrawler for {}".format(self._submission_title)

    def __len__(self):
        return len(self._submission.comments)


    def get_next_level_stats(self):
        logging.info("There are {} top comments".format(len(self)))
        for comment in self._submission.comments:
            logging.debug("Collecting stats for {}".format(comment.id))
            this_comment = CommentCalculator(comment.body)
            # all_stats = this_comment.get_all_stats()
            # msg = "Stats : {}".format(" ".join(["{}={}".format(k,all_stats[k]) for k in all_stats]))
            # print(msg)

            repeated_words = this_comment.get_repeated_word_count()
            msg = "".join(["\t{} : {}\n".format(word, repeated_words[word]) for word in repeated_words])
            print("All reapeated words:\n{}".format(msg))


    def _get_acceptable_submission(self):
        current_top_submissions = self._get_submissions()

        submission_id_map = {}

        # Pick an acceptable submission if it exists
        for submission in current_top_submissions:
            if len(submission.comments) < self._MAX_NUM_TOP_LEVEL_COMMENTS:
                submission_id_map[submission.id] = len(submission.comments)
            else:
                return submission  # TODO don't split the returns

        warning_msg = "No submission in the top {} sorted by {} with at least {} comments".format(
            self._MAX_NUM_TOP_LEVEL_COMMENTS,
            self.comment_ordering,
            self._MAX_NUM_TOP_LEVEL_COMMENTS
        )
        warnings.warn(warning_msg)
        logging.warning(warning_msg)

        best_id = self._get_best_option(submission_id_map)
        return self.read_only_reddit.submission(id=best_id)

    def _get_best_option(self, sub_dict):
        max = 0
        best_option = None

        for submission_id in sub_dict:
            if sub_dict[submission_id] > max:
                max = sub_dict[submission_id]
                best_option = submission_id

        if best_option:
            return best_option
        else:
            raise RuntimeError("No submission found in the top {} sorted by {}".format(
                self._MAX_NUM_TOP_LEVEL_COMMENTS,
                self.comment_ordering))

    def _get_submissions(self):
        output = {
            'hot': self.sub.hot(limit=self._MAX_SUBMISSIONS_SEARCH),
            'top': self.sub.top('day'),
            'new': self.sub.new(limit=self._MAX_SUBMISSIONS_SEARCH)
        }

        return output[self.comment_ordering]
