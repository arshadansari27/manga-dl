import sqlite3


class DB:
    def __init__(self, database='manga.db'):
        try:
            self.conn = sqlite3.connect(database)
        except:
            print "Error occured when opening the connection"

    def close(self):
        try:
            self.conn.close()
        except:
            print "Error occured when closing the connection"

    def executeOne(self, sql):
        return self.conn.execute(sql)

    def executeMany(self, sql, datas):
        return self.conn.executemany(sql, datas)


class Node:

    def __init__(self, title, link, feed_name='magi_the_labyrinth_of_magic.xml'):
        index = -1
        ch = title[index]
        while ch != ' ':
            index -= 1
            ch = title[index]
        self.id = title[index + 1:]
        self.title = title
        self.link = link
        self.done = False
        self.pages = []
        self.feed_name = feed_name


class Page:
    def __init__(self, node):
        pass
