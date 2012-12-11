from feed_reader import get_feed, get_image_and_next_link
import sqlite3
import urllib2


def update_db_with_latest_feed(conn, xml):
    c = conn.cursor()
    rows = c.execute("select max(id) from node")
    (id, ) = rows.fetchone()
    print id
    nodes = get_feed(xml)
    node_values = []
    for node in nodes:
        if node.id <= id:
            continue
        print node.id
        print node.title
        print node.link
        print "*************************"
        node_values.append((node.id, node.title, node.link, node.done, node.feed_name,))

    if len(node_values) > 0:
        if id is None:
            c.execute("create table node (id text, title text, link text, done text, feed_name text)")
        c.executemany('insert into node values (?, ?, ?, ?, ?)', node_values)
        conn.commit()


def get_pages_for_existing_feed(conn):
    c = conn.cursor()
    rows = c.execute("select id, title, link from node where done = '0'")
    for row in rows:
        (id, title, link) = row
        print link
        page = urllib2.urlopen(link)
        if not (page.code >= 200 and page.code < 300):
            raise Exception("Damn page was not downloaded")
        content = page.read()
        if content is not None and len(content) > 0:
            (next_link, image) = get_image_and_next_link(content, link)

    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect('manga.db')
    update_db_with_latest_feed(conn, 'magi_the_labyrinth_of_magic.xml')
    print "**********************GETING PAGES"
    get_pages_for_existing_feed(conn)
    conn.close()
