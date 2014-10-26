# -*- coding:utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import enum

class statics_plot():

  Type = enum.Enum('Type', 'line plot bar');

  # Format of item in items is dictionary, key:date value:data
  @classmethod
  def generate_statics_image(cls, items, since, latest, days=1, type=Type.line, folder='images/', color='r'):
    x_label, statics = cls.generate_sum(items, since, latest, days=days)
    fig = plt.figure()
    graph = fig.add_subplot(111)
    # plot type
    if type==cls.Type.line:
        graph.plot(x_label, list(statics.values()), color=color)
    elif type==cls.Type.plot:
        graph.plot(x_label, list(statics.values()), 'o', color=color)
    elif type==cls.Type.bar:
        graph.bar(x_label, list(statics.values()), color=color, edgecolor='k')
    else:
        print("Error: "+type+" does not match any of Type enum.")

    # graph format for days
    days = mdt.DayLocator() # every day
    daysFormat = mdt.DateFormatter('%Y-%m-%d')
    graph.xaxis.set_major_locator(days)
    graph.xaxis.set_major_formatter(daysFormat)
    fig.autofmt_xdate()

    # Generate graph image file
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_path = folder+now+'.png'
    plt.savefig(file_path)

    return file_path

  @classmethod
  def generate_sum(cls, items, since, latest, days=1):
    x_label = cls.generate_date_label(since, latest, days=days)
    return list(reversed(x_label[1:])), {x_label[i]:len([k for k,v in items.items() if x_label[i] < k and k < x_label[i-1]]) for i in range(len(x_label)-1, 0, -1)}

  @classmethod
  def generate_date_label(cls, since, latest, days=1):
    return [latest - datetime.timedelta(days=x) for x in range(0, (latest-since).days, days)]
