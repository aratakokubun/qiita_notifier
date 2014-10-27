# -*- coding:utf-8 -*-

from qiita import *
from datetime import datetime, timedelta
import ConfigParser
import pytz

class qiita_handler():

  # Constants
  config_file = 'qiita.cfg'
  target_section = 'qiita'
  default_config = {
    'user_name': 'null',
    'user_pass': 'null',
  }

  def __init__(self):
    self.set_config()
    self.do_oauth()
    self.update = datetime.strptime('2000/01/01', '%Y/%m/%d')

  def __del__(self):
    pass

  def set_config(self):
    try:
      self.config = ConfigParser.SafeConfigParser(self.default_config)
      self.config.read(self.config_file)
      if not self.config.has_section(self.target_section):
        self.config.add_section(self.target_section)

      self.user_name    = self.config.get(self.target_section, 'user_name')
      self.user_pass    = self.config.get(self.target_section, 'user_pass')
    except:
      print "Could not read config file : %s" % self.config_file

  def do_oauth(self):
    try:
      self.client = Client(url_name = self.user_name, password = self.user_pass)
      self.token = self.client.token # -> contains token
    except:
      print "Oauth failed with name:%s, pass:%s" % (self.user_name, self.user_pass)

  # formae : title:string, body:string, tags:dictionary[name, versions], private:boolean
  def post(self, title, body, tags, private):
    params = {
      'title' : title,
      'body' : body,
      'tags' : tags,
      'private' : private
    }
    client = Client(token=self.token)
    items = client.post_item(params)

  def update_posts(self, page=1, nums=100):
    client = Users()
    self.user_items = client.user_items(url_name=self.user_name, params={'page':page, 'per_page':nums})
    self.update = datetime.now()

  def get_items_from(self, since_dt, nums=100):
    all_items = []
    oldest_dt = datetime.now()
    page = 1
    while oldest_dt > since_dt:
      self.update_posts(page=page, nums=nums)
      if len(self.user_items) == 0:
          break
      all_items += self.user_items
      oldest_dt = self.str_to_datetime(self.user_items[-1]['created_at'])
      page += 1
    return all_items

  def get_latest_post(self):
      self.update_posts(nums=1)
      return self.user_items[0]

  def get_latest_post_time(self):
    self.update_posts(nums=1)
    return self.str_to_datetime(self.user_items[0]['created_at'])

  def get_today_post_items(self):
    self.update_posts()
    return [item for item in self.user_items if (datetime.now() - self.str_to_datetime(item['created_at'])).days < 1]

  def get_weekly_post_items(self):
    weekly_items = self.get_items_from(datetime.now()-timedelta(8))
    # return [item for item in weekly_items if (datetime.now() - self.str_to_datetime(item['created_at'])).days < 8]
    return {self.str_to_datetime(item['created_at']):item for item in weekly_items if (datetime.now() - self.str_to_datetime(item['created_at'])).days < 8}

  def get_monthly_post_items(self):
    monthly_items = self.get_items_from(datetime.now()-timedelta(31))
    return {self.str_to_datetime(item['created_at']):item for item in monthly_items if (datetime.now() - self.str_to_datetime(item['created_at'])).days < 31}

  def get_yearly_post_items(self):
    yearly_items = self.get_items_from(datetime.now()-timedelta(365))
    return {self.str_to_datetime(item['created_at']):item for item in yearly_items if (datetime.now() - self.str_to_datetime(item['created_at'])).days < 365}

  def str_to_datetime(self, time_str):
    # qiita created_at format 2000-01-01 00:00:00 +0900
    # return datetime.strptime(time_str[:-6], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
    return datetime.strptime(time_str[:-6], '%Y-%m-%d %H:%M:%S')
