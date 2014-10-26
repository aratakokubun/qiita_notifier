# -*- coding:utf-8 -*-

import tweepy
import random
import sys
import ConfigParser

class twitter_handler():
  config_file = 'twitter.cfg'
  debug = True
  target_test = 'otenki'
  target_section = 'kokushingo'

  default_config = {
    'since_id': '1',
    'consumer_key': 'null',
    'consumber_secred': 'null',
    'access_key': 'null',
    'access_secret': 'null',
  }

  def __init__(self):
    self.target = self.target_test if self.debug else self.target_section
    self.set_config()
    self.do_oauth()

  def set_config(self):
    try:
      self.config = ConfigParser.SafeConfigParser(self.default_config)
      self.config.read(self.config_file)
      if not self.config.has_section(self.target):
        self.config.add_section(self.target)

      # read data from config file
      self.since_id = self.config.getint(self.target, 'since_id')
      self.consumer_key = self.config.get(self.target, 'consumer_key')
      self.consumer_secret = self.config.get(self.target, 'consumer_secret')
      self.access_key = self.config.get(self.target, 'access_key')
      self.access_secret = self.config.get(self.target, 'access_secret')
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

  # post single item
  def post(self, str):
    self.api.update_status(str.decode('utf-8').strip())

  # post single item with media
  def post_with_media(self, status, file):
    # self.api.status_update_with_media(file, status=status)
    self.api.update_with_media(file, status=status)

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
