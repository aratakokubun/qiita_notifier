	# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
import ConfigParser
from qiita_handler import qiita_handler as qih
from twitter_handler import twitter_handler as twh
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

  auto_msg = '[Auto] '
  urge_post_msg = 'You did not upload any post to qiita %s. You should do some action tomorrow!'
  complete_post_msg = 'You have uploaded "%s" %s. Keep going on!'
  static_msg = 'Your action in %s'

  def __init__(self):
    self.set_config()
    self.qih = qih()
    self.twh = twh()
    self.stp = stp()

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

    if (now-self.update_day).days < 1:
        return

    latest_post = self.qih.get_latest_post()
    latest_time = self.str_to_datetime(latest_post['created_at'][:-6])
    date_diff = datetime.now() - latest_time
    if date_diff.days > 6:
        self.twh.post_to_myself(self.urge_post_msg % ('in this week'))
    elif date_diff.days > 0:
        self.twh.post_to_myself(self.urge_post_msg % ('today'))
    else:
        self.twh.post_to_myself(self.complete_post_msg % (latest_post['title'], 'today'))
    # update config update_day
    self.config.set(self.target_section, 'update_day', self.datetime_to_str(now))
    self.config.write(open(self.config_file, 'w'))

  def post_weekly_statics(self):
    now = datetime.now()

    if (now-self.update_week).days < 7:
        return

    since = now - timedelta(8)
    weekly_items = self.qih.get_weekly_post_items()

    if len(weekly_items) == 0:
        return

    # file = stp.generate_statics_image(weekly_items, since, now, type=stp.Type.bar, folder='images/week-')
    # self.twh.post_with_media(self.static_msg % ('this week'), file)
    file = self.stp.generate_statics_plotly(weekly_items, since, now, file='weekly_statics')
    self.twh.post_to_myself(self.static_msg % ('this week') + '\n' + file)
    # update config update_day
    self.config.set(self.target_section, 'update_week', self.datetime_to_str(now))
    self.config.write(open(self.config_file, 'w'))

  def post_monthly_statics(self):
    now = datetime.now()

    if (now-self.update_month).days < 31:
        return

    since = now - timedelta(31)
    monthly_items = self.qih.get_monthly_post_items()

    if len(monthly_items) == 0:
        return

    # file = stp.generate_statics_image(monthly_items, since, now, days=3, type=stp.Type.bar, folder='images/month-')
    # self.twh.post_with_media(self.static_msg % ('this month'), file)
    file = self.stp.generate_statics_plotly(monthly_items, since, now, days=3, file='monthly_statics')
    self.twh.post_to_myself(self.static_msg % ('this month') + '\n' + file)
    # update config update_day
    self.config.set(self.target_section, 'update_month', self.datetime_to_str(now))
    self.config.write(open(self.config_file, 'w'))

  def post_yearly_statics(self):
    now = datetime.now()

    if (now-self.update_month).days < 365:
        return

    since = now - timedelta(365)
    yearly_items = self.qih.get_yearly_post_items()

    if len(yearly_items) == 0:
        return

    # file = stp.generate_statics_image(yearly_items, since, now, days=30, type=stp.Type.bar, folder='images/year-')
    # self.twh.post_with_media(self.static_msg % ('this year'), file)
    file = self.stp.generate_statics_plotly(yearly_items, since, now, days=30, file='yearly_statics')
    self.twh.post_to_myself(self.static_msg % ('this year') + '\n' + file)
    # update config update_day
    self.config.set(self.target_section, 'update_year', self.datetime_to_str(now))
    self.config.write(open(self.config_file, 'w'))

  # -------------------------------------------------------------------------
  def str_to_datetime(self, time_str):
    # qiita created_at format 2000-01-01 00:00:00 +0900
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

  def datetime_to_str(self, dt):
    # qiita created_at format 2000-01-01 00:00:00 +0900
    return dt.strftime('%Y-%m-%d %H:%M:%S')
