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
  complete_post_msg = 'You have uploaded "%s"(%s) %s. Keep going on!'
  static_msg = 'Your action of Qiita in %s'

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

    if (now-self.update_day).seconds/3600 + (now-self.update_day).days*24 < 23:
        print("Not a day has passed since last update.")
        return

    latest_post = self.qih.get_latest_post()
    latest_time = self.str_to_datetime(latest_post['created_at'][:-6])
    date_diff = datetime.now() - latest_time
    if date_diff.days > 0:
        post_msg = self.urge_post_msg % ('in %d days!' % (date_diff.days))
    else:
        post_msg = self.complete_post_msg % (latest_post['title'], latest_post['url'], 'today')
    self.twh.post_to_myself(post_msg)
    print('tweet msg:%s' % post_msg)
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
