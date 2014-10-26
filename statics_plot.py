# -*- coding:utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib.date as mdt

class statics_plot():

  def __init__(self):
    pass

  def __del__(self):
    pass
  # Format of item in items is dictionary, key:date value:data
  def generate_static_image(self, items, since, latest, days=1):
    x_label, statics = generate_sum(items, since, latest, days=days)
    fig = plt.figure()
    graph = fig.add_subplot(111)
    graph.plot(x_label, statics)

    # graph format for days
    days = mdt.DayLocator() # every day
    daysFormat = mdt.DateFormatter('%Y-%m-%d')
    graph.xaxis.set_major_locator(days)
    graph.xaxis.set_major_formatter(daysFormat)
    fig.autofmt_xdate()

    # Generate graph image file
    now = datetime.now().date()
    file_path = 'images/'+now+'.png'
    plt.savefig(file_path)

    return file_path

  def generate_sum(self, items, since, latest, days=1):
    x_label = generate_date_label(since, latest, days=days)
    # return x_label, {x_label[i]:len([k for k,v in items.iteritems() if x_label[i] < k && k < x_label[i-1]]) for i in range(len(x_label)-1, 0, -1)}
    return x_label, x_label

  def generate_date_label(self, since, latest, days=1):
    return [latest - datetime.timedelta(days=x) for x in range(-1, (latest-since).days, days)]
