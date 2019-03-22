import warnings
import logging

from RedditCollectionService.praw_adapter import PrawDapter
from RedditCollectionService.comment_calculator import CommentCalculator

MAX_SUBMISSIONS_SEARCH = 30
MIN_NUM_TOP_LEVEL_COMMENTS = 10
MAX_COMMENT_BRANCHES = 100


class SubmissionStats(object):
    """
    Returns data relating adjacent comment levels for the first acceptable submission.

    DEFINE ACCEPTABLE SUBMISSION
    """

    def __init__(self, subreddit):
        self._subreddit_name = subreddit
        prawdapter = PrawDapter()
        self._read_only_reddit = prawdapter.make_connection('read_only')
        self.sub = self._read_only_reddit.subreddit(self._subreddit_name)

        self.comment_ordering = 'hot'

        logging.info("Looking for acceptable submission in {}".format(self._subreddit_name))
        self._submission = self._get_acceptable_submission()
        logging.info("Found submission with {} top comments".format(len(self)))

        self._depth = 0
        self._current_id = self._submission.id

    def __str__(self):
        return "SubmissionStats for \"{}\"".format(self._submission.title)

    def __len__(self):
        return len(self._submission.comments)

    def spew_all_data(self):
        all_children = self._submission.comments.replace_more(limit=MAX_COMMENT_BRANCHES)
        # this needs to not be explicit for submission

        for ordered_comment_id in range(len(self)):
            # for comment in self._submission.comments:
            logging.debug("[{}] Collecting stats...".format(ordered_comment_id))
            comment = self._submission.comments[ordered_comment_id]
            logging.debug("[{}] Finished collecting stats for {}".format(ordered_comment_id, comment.id))
            this_comment = CommentCalculator(comment.body)
            # all_stats = this_comment.get_all_stats()
            # msg = "Stats : {}".format(" ".join(["{}={}".format(k,all_stats[k]) for k in all_stats]))
            # print(msg)

            all_stats = this_comment.get_all_single_stats()
            msg = "".join(["\t{} : {}\n".format(word, all_stats[word]) for word in all_stats])
            print("All stats for ordered comment {}:\n{}".format(ordered_comment_id, msg))

    def _get_acceptable_submission(self):
        current_top_submissions = self._get_submissions()

        submission_id_map = {}

        # Pick an acceptable submission if it exists
        for submission in current_top_submissions:
            if len(submission.comments) < MIN_NUM_TOP_LEVEL_COMMENTS:
                submission_id_map[submission.id] = len(submission.comments)
            else:
                return submission  # TODO don't split the returns

        best_id = self._get_best_option(submission_id_map)
        return self._read_only_reddit.submission(id=best_id)

    def _get_best_option(self, sub_dict):
        warning_msg = "No submission in the top {} sorted by {} with at least {} comments".format(
            MIN_NUM_TOP_LEVEL_COMMENTS,
            self.comment_ordering,
            MIN_NUM_TOP_LEVEL_COMMENTS)
        warnings.warn(warning_msg)
        logging.warning(warning_msg)

        max_number_of_comments = 0
        best_option = None

        for submission_id in sub_dict:
            if sub_dict[submission_id] > max_number_of_comments:
                max_number_of_comments = sub_dict[submission_id]
                best_option = submission_id

        if best_option:
            return best_option
        else:
            raise RuntimeError("No submission found in the top {} sorted by {}".format(
                MAX_SUBMISSIONS_SEARCH,
                self.comment_ordering))

    def _get_submissions(self):
        output = {
            'hot': self.sub.hot(limit=MAX_SUBMISSIONS_SEARCH),
            'top': self.sub.top('day'),
            'new': self.sub.new(limit=MAX_SUBMISSIONS_SEARCH)
        }

        return output[self.comment_ordering]
