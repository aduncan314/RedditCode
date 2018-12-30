import praw
import json
import logging

from os import environ, path


class RedditConnectionMaker(object):
    try:
        _system_user = environ['RedditCode.User'] # TODO: this may not need to be environment var; pass in init?
    except KeyError:
        print('Setting user to default')
        _system_user = 'default'

    def __init__(self):

        self.config = self._load_configuration()

    def make_connection(self, connection_type):
        conn_type = {
            'read_only': self._make_read_only_conn,
            'authorized': self._make_auth_conn
        }

        if connection_type not in list(conn_type):
            msg = "The only connection types are '{}' and '{}'".format(conn_type[0], conn_type[1])
            logging.error(msg)
            raise RuntimeError(msg)

        reddit_connection = conn_type[connection_type]()
        logging.info("{} Reddit instance created".format(connection_type))
        return reddit_connection

    def _make_read_only_conn(self):
        reddit = praw.Reddit(client_id=self.config['client_id'],
                             client_secret=self.config['client_secret'],
                             user_agent=self.config['user_agent'])
        reddit.read_only = True

        return reddit

    def _make_auth_conn(self):
        # TODO: does an error need to be caught here in order to not expose passwords etc?
        return praw.Reddit(client_id=self.config['client_id'],
                           client_secret=self.config['client_secret'],
                           user_agent=self.config['user_agent'],
                           username=self.config['username'],
                           password=self.config['password'])

    def _load_configuration(self):
        base_path = environ['RedditCode.BasePath']
        config_path = path.join(base_path, 'config.json')
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        if len(config[self._system_user]) < 1:
            raise RuntimeError("Configuration file for user, {}, is empty".format(self._system_user))
        else:
            return config[self._system_user]


def connection_factory(conn_type):
    connector = RedditConnectionMaker()
    reddit_instance = connector.make_connection(conn_type)
    return reddit_instance
