	# -*- coding:utf-8 -*-

from datetime import datetime
import ConfigParser
import qiita_handler
import twitter_handler

class qiita_notifier():

  # Constants
  config_file = 'application.cfg'
  target_section = 'update'
  default_config = {
    'since_id' : '1',
    'update_day': 'null',
    'update_week': 'null',
    'update_month': 'null',
    'update_year': 'null',
  }

  urge_post_msg = 'You did not upload any post to qiita %s. You should do something today!'
  complete_post_msg = 'You have uploaded "%s" %s. Keep going on!'

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

      self.since_id     = self.config.getint(self.target_section,  'since_id')
      self.update_day   = self.str_to_datetime(self.config.get(self.target_section,     'update_day'))
      self.update_week  = self.str_to_datetime(self.config.get(self.target_section,     'update_week'))
      self.update_month = self.str_to_datetime(self.config.get(self.target_section,     'update_month'))
      self.update_year  = self.str_to_datetime(self.config.get(self.target_section,     'update_year'))
    except:
      print "Could not read config file : %s" % self.config_file

  # -------------------------------------------------------------------------
  # Notify activity methods
  def post_today_action_to_twitter(self):
    self.qih.get_today_post_items()
    pass

  def check_qiita_action(self):
    latest_post = self.qih.get_latest_post()
    latest_time = self.str_to_datetime(latest_post['created_at'][:-6])
    date_diff = datetime.now() - latest_time
    if date_diff.days > 6:
        self.twh.post(urge_post_msg % ('in this week'))
    elif date_diff.days > 0:
        self.twh.post(urge_post_msg % ('today'))
    else:
        self.twh.post(complete_post_msg % (latest_post['title'], 'today'))

# -------------------------------------------------------------------------
  def str_to_datetime(self, time_str):
    # qiita created_at format 2000-01-01 00:00:00 +0900
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
