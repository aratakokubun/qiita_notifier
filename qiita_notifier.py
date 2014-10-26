	# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
import ConfigParser
import qiita_handler
import twitter_handler
from statics_plot import statics_plot as stp

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

  urge_post_msg = 'You did not upload any post to qiita %s. You should do some action tomorrow!'
  complete_post_msg = 'You have uploaded "%s" %s. Keep going on!'
  static_msg = 'Your action in %s'

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
      print("Could not read config file : %s" % self.config_file)

  # -------------------------------------------------------------------------
  def check_qiita_action(self):
    now = datetime.now()

    if (now-self.update_day).days > 0:
        latest_post = self.qih.get_latest_post()
        latest_time = self.str_to_datetime(latest_post['created_at'][:-6])
        date_diff = datetime.now() - latest_time
        if date_diff.days > 6:
            self.twh.post(self.urge_post_msg % ('in this week'))
        elif date_diff.days > 0:
            self.twh.post(self.urge_post_msg % ('today'))
        else:
            self.twh.post(self.complete_post_msg % (latest_post['title'], 'today'))
        # update config update_day
        self.config.set(self.target_section, 'update_day', self.datetime_to_str(now))
        self.config.write(open(self.config_file, 'w'))

  def qiita_statics(self):
    pass

  def post_weekly_statics(self):
    now = datetime.now()
    since = now - timedelta(7)
    weekly_items = self.qih.get_weekly_post_items()
    file = stp.generate_statics_image(weekly_items, since, now, type=stp.Type.line)
    self.twh.post_with_media(self.static_msg % ('this week'), file)

  # -------------------------------------------------------------------------
  def str_to_datetime(self, time_str):
    # qiita created_at format 2000-01-01 00:00:00 +0900
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

  def datetime_to_str(self, dt):
    # qiita created_at format 2000-01-01 00:00:00 +0900
    return dt.strftime('%Y-%m-%d %H:%M:%S')
