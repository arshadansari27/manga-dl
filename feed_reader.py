from xml.dom.minidom import parse
from model import Node
from BeautifulSoup import BeautifulSoup
import re


def get_feed(xml):
    dom = parse(xml)
    nodes = []
    for element in dom.getElementsByTagName('item'):
        title = element.getElementsByTagName('title').item(0).childNodes[0].wholeText
        link = element.getElementsByTagName('link').item(0).childNodes[0].wholeText
        node = Node(title, link, xml)
        nodes.append(node)
    return nodes


def get_image_and_next_link(content, original_link):
    soup = BeautifulSoup(content)
    image = [str(img) for img in soup.findAll('img') if str(img).find('onerror') != -1][0]
    image = [val.split("=")[1][1:-1] for val in image.split() if val.find('src') != -1][0]
    next_page_tag = [str(link) for link in soup.findAll('a') if does_next_page_exists(link)][0]
    next_link_page = [link.split("=")[1][1:-1] for link in next_page_tag.split() if link.find("href") != -1][0]
    if not next_link_page[-4:] == 'html':
        return (None, image)

    idx = original_link.find('/')
    print idx
    while idx != -1:
        pos = idx + 1
        idx = original_link.find('/', idx + 1)
        print idx

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
