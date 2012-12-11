import sys
from feed_reader import setup_feed, setup_chapters, setup_pages
from image_downloader import download_images_for_feed

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage:\n\tpython main.py feed_name.xml http_link_for_xml_file output_folder"
        exit()
    feed_name = sys.argv[1]
    feed_link = sys.argv[2]
    output_folder = sys.argv[3]
    feed = setup_feed(feed_name, feed_link)
    chapters = setup_chapters(feed)
    if chapters is None:
        raise Exception("Why are chapters none?")
    pages = {}
    for chapter in chapters:
        pages[chapter.id] = setup_pages(chapter)

    download_images_for_feed(feed, output_folder)
