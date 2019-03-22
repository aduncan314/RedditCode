import logging
from os import path, environ

from RedditCodeLogging import initialize_logging
from RedditCollectionService.submission_stats import SubmissionStats

environ['RedditCode.Environment'] = 'TESTING'
environ['RedditCode.BasePath'] = path.abspath(path.dirname(__file__))

initialize_logging()

logging.info("Beginning RedditCode")

my_collector = SubmissionStats('pics')
my_collector.spew_all_data()
