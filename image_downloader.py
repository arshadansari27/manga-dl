from model import session, Chapter, Page
from threads import Job, RetryThread, RetrievalThread, FileSaveThread
import Queue
import os


def download_images_for_feed(feed, directory):
    url_queue = Queue.Queue()
    file_queue = Queue.Queue()
    failed_queue = Queue.Queue()
    update_queue = Queue.Queue()

    for i in range(10):
        urlThread = RetrievalThread(url_queue, file_queue, failed_queue)
        urlThread.setDaemon(True)
        urlThread.start()

    for i in range(2):
        fileThread = FileSaveThread(file_queue, update_queue)
        fileThread.setDaemon(True)
        fileThread.start()

    """for i in range(2):
        updateThread = UpdatePageThread(update_queue)
        updateThread.setDaemon(True)
        updateThread.start()"""

    retryThread = RetryThread(url_queue, failed_queue)
    retryThread.setDaemon(True)
    retryThread.start()

    if feed is None or feed.id is None:
        raise Exception("Feed cannot be null")
    if not os.path.exists(directory):
        os.makedirs(directory)
        print "Creating %s" % directory
    feed_dir = os.path.join(directory, feed.name.replace(' ', '_'))
    if not os.path.exists(feed_dir):
        os.makedirs(feed_dir)
        print "Creating %s " % feed_dir
    chapters = session.query(Chapter).filter(Chapter.feed_id == feed.id).all()
    for chapter in chapters:
        chapter_dir = os.path.join(feed_dir, chapter.title.replace(' ', '_'))
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
            print "Creating %s " % chapter_dir
        pages = session.query(Page).filter(Page.chapter_id == chapter.id).all()
        for page in pages:
            if page.downloaded or page.image_link is None:
                continue
            page_name = page.page_link[::-1]
            index = page_name.find('/')
            page_name = page_name[0:index][::-1]
            index = page_name.find('.html')
            page_file = os.path.join(chapter_dir, page_name[0:index]) + ".jpg"
            job = Job(page.id, page.image_link, page_file)
            url_queue.put(job)

    while True:
        job = update_queue.get()
        page = session.query(Page).filter(Page.id == job.page_id).first()
        page.downloaded = True
        session.add(page)
        session.commit()
        print "Page [%d] saved." % page.id
        update_queue.task_done
    url_queue.join()
    file_queue.join()
    failed_queue.join()
