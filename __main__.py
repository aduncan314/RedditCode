import logging
from os import path, environ

from RedditCodeLogging import initialize_logging
from RedditCollectionService.submission_crawler import SubmissionCrawler

environ['RedditCode.Environment'] = 'TESTING'
environ['RedditCode.BasePath'] = path.abspath(path.dirname(__file__))

initialize_logging()

logging.info("Beginning RedditCode")

my_collector = SubmissionCrawler('pics')
my_collector.get_next_level_stats()
