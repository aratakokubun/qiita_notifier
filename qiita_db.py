# -*- coding: utf-8 -*-

import sqlite3 as sqlite
import re

class mp3_db:

    def __init__(self, db_name):
        self.con = sqlite.connect(db_name)

    def __del__(self):
        self.con.close()

    # -----------------------------------------------------------------------
    # print
    def print_artist(self):
        res = self.con.execute("select * from artist order by id limit 200").fetchall()
        for item in res:
            try:
                print(item)
            except UnicodeEncodeError:
                self.con.execute("delete from artist where artist='%s'" % (item[1]))
    def print_music(self):
        res = self.con.execute("select * from music order by id").fetchall()
        for item in res:
            print(item)

    # -----------------------------------------------------------------------
    # search
    def search_artist(self, artist):
        artist = self.arrange_str(artist)
        res = self.con.execute("select * from artist where artist='%s'" % (artist)).fetchone()

        if res:
            return True
        else:
            return False

    def check_if_already_crawled(self, artist):
        artist = self.arrange_str(artist)
        res = self.con.execute("select * from artist where artist='%s' and crawled='1'" % (artist)).fetchone()

        if res:
            return True
        else:
            return False

    def search_music(self, artist, title):
        artist = self.arrange_str(artist)
        title = self.arrange_str(title)
        res = self.con.execute("select * from music where artist='%s' and title='%s'" % (artist, title)).fetchone()

        if res:
            return True
        else:
            return False

    # get first url
    def get_uncrawled_artists(self):
        res = self.con.execute("select artist, url from artist where crawled='0' order by id").fetchall()
        return res

    def get_uncrawled_musics(self):
        res = self.con.execute("select * from music where crawled='0' order by id").fetchall()
        return res

    # -----------------------------------------------------------------------
    # add
    def add_artist(self, artist, url):
        artist = self.arrange_str(artist)

        if self.search_artist(artist):
            return False
        else:
            self.con.execute("insert into artist (artist, url, crawled) values ('%s', '%s', %d)" % (artist, url, 0))
            self.con.commit()
            return True

    def add_music(self, artist, title, url):
        artist = self.arrange_str(artist)
        title = self.arrange_str(title)

        if self.search_music(artist, title):
            return False
        else:
            self.con.execute("insert into music (artist, title, url, crawled) values ('%s', '%s', '%s', %d)" % (artist, title, url, 0))
            self.con.commit()
            return True

    # crawl
    def crawl_artist(self, artist, url, flag = 1):
        artist = self.arrange_str(artist)

        if self.search_artist(artist):
            self.con.execute("update artist set crawled=%d where artist='%s'" % (flag, artist))
        else:
            self.con.execute("insert into artist (artist, url, crawled) values ('%s', '%s', %d)" % (artist, url, flag))
        self.con.commit()

    def crawl_music(self, artist, title, url, flag = 1):
        artist = self.arrange_str(artist)
        title = self.arrange_str(title)

        if self.search_music(artist, title):
            self.con.execute("update music set crawled=%d where artist='%s' and title='%s'" % (flag, artist, title))
        else:
            self.con.execute("insert into music (artist, title, url, crawled) values ('%s', '%s', '%s', %d)" % (artist, title, url, flag))
        self.con.commit()

    def delete_uncrawled(self):
        self.con.execute("delete from artist where crawled='0'")
        self.con.execute("delete from music where crawled='0'")
        self.con.commit()

    # -----------------------------------------------------------------------
    # artist names are arranged with small letters of alphabets and numbers, others are discareded
    def arrange_str(self, str):
        sqlitter = re.compile('\\W*')
        return "".join([s.lower() for s in sqlitter.split(str) if s!=''])

    # -----------------------------------------------------------------------
    def make_tables(self):
        self.con.execute("create table artist(id integer PRIMARY KEY, artist text, url text, crawled integer)")
        self.con.execute("create table music(id integer PRIMARY KEY, artist text, title text, url text, crawled integer)")
        self.con.commit()

    def clear_tables(self):
        self.con.execute("delete from artist")
        self.con.execute("delete from music")
        self.con.commit()
