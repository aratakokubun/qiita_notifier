# -*- coding:utf-8 -*-
from qiita import *

if __name__ == "__main__":
  # get user's item
  print("get user name")
  client = Users()
  items = client.user_items('heavenshell')
  for item in items:
    print(item)

  # get tag's item
  print("get tag item")
  client = Tags()
  items = client.tag_items('python')
  for item in items:
    print(item)

  # get specified item with comments and raw markdown content
  client = Items()
  item_uuid = 'input item uuid in qiita'
  items = client.item(item_uuid)
  for item in item:
    print(item)

  # Authentification
  client = Client(url_name = 'user_name', password = 'user password')
  token = client.token # -> contains token
  # or client = Client(token='user auth token')

  # Get my items
  client = Client(token='my auth token')
  items = client.user_item()

  # Post and Delete
  client = Client(token='my oauth token')
  params = {
    'title' : 'Hello',
    'body' : 'markdown text',
    'tags' : [{name: 'python', versions: ['2.6', '2.7']}],
    'private' : false
  }
  # do post
  items = client.post_item(params)
  # do update
  params['title'] = 'change items'
  client.update_item(Item['uuid'], params)
  # do delete
  client.delete_item()

  # stock and unstock items
  client = Items(token='my oauth token')
  uuid = 'uuid of item'
  # do stock
  client.stock_item(item_uuid)
  # do unstock
  client.unstock_item(item_uuid)
