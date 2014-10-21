# -*- coding:utf-8 -*-

import tweepy
import random
import sys
import ConfigParser

class twitter_handler():
  config_file = 'twitter.cfg'
  target_section = 'twitter'

  default_config = {
    'since_id': '1',
    'consumer_key': 'null',
    'consumber_secred': 'null',
    'access_key': 'null',
    'access_secret': 'null',
  }

  def __init__(self):
    self.set_config()
    self.do_oauth()

  def set_config(self):
    try:
      self.config = ConfigParser.SafeConfigParser(self.default_config)
      self.config.read(self.config_file)
      if not self.config.has_section(self.target_section):
        self.config.add_section(self.target_section)

      # read data from config file
      self.since_id = self.config.getint(self.target_section, 'since_id')
      self.consumer_key = self.config.get(self.target_section, 'consumer_key')
      self.consumer_secret = self.config.get(self.target_section, 'consumer_secret')
      self.access_key = self.config.get(self.target_section, 'access_key')
      self.access_secret = self.config.get(self.target_section, 'access_secret')
    except:
      print "Could not read config file : %s" % (self.config_file)

  # Do twitter outhentification
  def do_oauth(self):
    # create ouath handler
    self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret);
    # set access token to oauth handler
    self.auth.set_access_token(self.access_key, self.access_secret);
    # create api
    self.api = tweepy.API(auth_handler = self.auth);


  def post(self, str):
    api.update_status(str.decode('utf-8').strip())

  # Update since_id in config file
  def update_config(self):
    try:
      self.config.set(self.target_section, 'since_id', str(self.since_id))
      self.config.write(open(self.otenki_config_file, 'w'))
    except:
      print "Error: Could not write to config: %s", (self.default_config_file)
      sys.exit(1)

  # Tweet all items in list
  def tweet_posts(self, posts):
    for post in posts:
      length = len(post)
      if length > 140:
        self.api.update_status(post[:140])
      else:
        self.api.update_status(post)
