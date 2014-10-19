# -*- coding:utf-8 -*-

from datetime import datetime
import post_twitter
import qiita_handler
import twitter_handler

class qiita_notifier():

  # Constants
  config_file = 'qiita.cfg'
  target_section = 'update'
  default_config = {
    'since_id' : '1',
    'update_day': 'null',
    'update_week': 'null',
    'update_month': 'null',
    'update_year': 'null',
  }

  def __init__(self):
    self.set_config()
    self.qih = qiita_handler.qiita_handler()
    self.twh = twitter_handler.twitter_handler()

  def set_config(self):
    try:
      self.config = ConfigParser.SafeConfigParser(self.default_config)
      self.config.read(self.config_file)
      if not self.config.has_section(self.target_section):
        self.config.add_section(self.target_section)

      self.since_id     = self.str_to_datetime(self.config.getint(self.target_section,  'since_id'))
      self.update_day   = self.str_to_datetime(self.config.get(self.target_section,     'update_day'))
      self.update_week  = self.str_to_datetime(self.config.get(self.target_section,     'update_week'))
      self.update_month = self.str_to_datetime(self.config.get(self.target_section,     'update_month'))
      self.update_year  = self.str_to_datetime(self.config.get(self.target_section,     'update_year'))
    except:
      print "Could not read config file : %s" % self.config_file

  def post_today_action_to_twitter(self):
    pass

  def str_to_datetime(self, time_str):
    # qiita created_at format 2000-01-01 00:00:00 +0900
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
