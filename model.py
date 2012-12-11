class DB:
    pass


class Feed:

    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.nodes = []

    def add_node(self, title, page_link):
        node = Node(title, page_link, self.name)
        self.nodes.append(node)


class Node:

    def __init__(self, title, link, feed_name):
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

    def add_page(self, link, image, next_link):
        page = Page(self.id, link, image, next_link)
        self.pages.append(page)


class Page:
    def __init__(self, node_id, link, image, next_link):
        self.node_id = node_id
        self.link = link
        self.image = image
        self.next_link = next_link
