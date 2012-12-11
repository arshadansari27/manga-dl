import sys
from feed_reader import setup_feed, setup_chapters, setup_pages


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage:\n\tpython main.py feed_name.xml http_link_for_xml_file"
        exit()
    feed_name = sys.argv[1]
    feed_link = sys.argv[2]
    feed = setup_feed(feed_name, feed_link)
    chapters = setup_chapters(feed)
    if chapters is None:
        raise Exception("Why are chapters none?")
    pages = {}
    for chapter in chapters:
        pages[chapter.id] = setup_pages(chapter)
    for key, value in pages:
        print str(key) + "=>" + str([str(v) + "\n" for v in value])
