from xml.dom.minidom import parseString
from model import Feed, session, Chapter, Page
from BeautifulSoup import BeautifulSoup
import urllib2
import re


def setup_feed(feed_name, feed_link):
    xml = download_feed_xml(feed_link)
    feed = get_feed_from_db(feed_name)
    if feed is not None:
        feed.xml = compare_return_latest(feed.xml, xml)
    else:
        feed = Feed(name=feed_name, link=feed_link, xml=xml)
        session.add(feed)
        print "Added Feed %s" % feed.name
        session.flush()
        session.commit()
    return feed


def get_feed_from_db(feed_name):
    feed = session.query(Feed).filter(Feed.name == feed_name).first()
    if feed is not None:
        print feed.xml
    return feed


def download_feed_xml(feed_link):
    response = urllib2.urlopen(feed_link)
    if not (response.code >= 200 and response.code < 300):
        raise Exception("Could not retrieve the given link for feed. %s" % feed_link)
    print "Downloading feed from %s" % feed_link
    return response.read()


def compare_return_latest(db_xml, dload_xml):
    if len(db_xml) != len(dload_xml):
        return dload_xml
    elif db_xml != dload_xml:
        return dload_xml
    else:
        return db_xml


def setup_chapters(feed):
    dom = parseString(feed.xml)
    nodes = session.query(Chapter).filter(Chapter.feed_id == feed.id).all()
    node_dict = {}
    for node in nodes:
        node_dict[node.title] = True

    for element in dom.getElementsByTagName('item'):
        title = element.getElementsByTagName('title').item(0).childNodes[0].wholeText
        link = element.getElementsByTagName('link').item(0).childNodes[0].wholeText
        if node_dict.get(title, None) is not None:
            continue
        node = Chapter(title, link, feed)
        session.add(node)
        session.commit()
        print "Added Chapter %s" % node.title
        page = Page(link, node)
        session.add(page)
        session.commit()
        print "Added Page[%d] %s" % (page.id, page.page_link)
    return session.query(Chapter).filter(Chapter.feed_id == feed.id).all()


def setup_pages(chapter):
    pages = session.query(Page).filter(Page.chapter_id == chapter.id).all()
    if pages is None:
        return None
    for page in pages:
        if page.page_link is None:
            raise Exception("How could page link be none")
        if page.next_page_id is not None:
            continue
        update_page(page, chapter)
    return session.query(Page).filter(Page.chapter_id == chapter.id).all()


def update_page(page, chapter):
    print "Calling %s" % page.page_link
    response = urllib2.urlopen(page.page_link)
    if not (response.code >= 200 and response.code < 300):
        raise Exception("Could not retrieve the page for link . %s" % page.page_link)
    print "Response %s" % response.code
    content = response.read()
    (next_link, image) = get_image_and_next_link(content, page.page_link)
    while next_link is not None:
        if image is None:
            raise Exception("Something went wrong with the lack of image for given page")
        page.image_link = image
        next_page = Page(next_link, chapter)
        session.add(next_page)
        session.commit()
        print "Added Page[%d] %s" % (next_page.id, next_page.page_link)
        page.next_page_id = next_page.id
        session.add(page)
        session.commit()
        print "Update page %d with image %s" % (page.id, page.image_link)
        page = next_page
        response = urllib2.urlopen(page.page_link)
        if not (response.code >= 200 and response.code < 300):
            raise Exception("Could not retrieve the page for link . %s" % page.page_link)
        content = response.read()
        (next_link, image) = get_image_and_next_link(content, page.page_link)


def get_image_and_next_link(content, original_link):
    soup = BeautifulSoup(content)
    image = [str(img) for img in soup.findAll('img') if str(img).find('onerror') != -1][0]
    image = [val.split("=")[1][1:-1] for val in image.split() if val.find('src') != -1][0]
    next_page_tag = [str(link) for link in soup.findAll('a') if does_next_page_exists(link)][0]
    next_link_page = [link.split("=")[1][1:-1] for link in next_page_tag.split() if link.find("href") != -1][0]
    if not next_link_page[-4:] == 'html':
        return (None, image)

    idx = original_link.find('/')
    while idx != -1:
        pos = idx + 1
        idx = original_link.find('/', idx + 1)

    return (original_link[:pos] + next_link_page, image)


def does_next_page_exists(link):
    if link is None:
        return False
    match = re.search('next_page', str(link))
    if match is None:
        return False
    if match.group() == 'next_page':
        return True
    else:
        return False
