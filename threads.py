from model import session, Page
import urllib2
import threading


class Job:

    def __init__(self, page_id, download_link, file_name):
        self.page_id = page_id
        self.count = 0
        self.download_link = download_link
        self.file_name = file_name
        self.content = None

    def done(self, content):
        self.content = content


class RetrievalThread(threading.Thread):

    def __init__(self, url_queue, file_queue, failed_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.file_queue = file_queue
        self.failed_queue = failed_queue

    def run(self):
        while True:
            job = self.url_queue.get()
            job.count += 1
            print "Trying to download %s %s" % (job.download_link, job.count == 1 and "for the first time" or "for the %d time" % job.count)
            try:
                response = urllib2.urlopen(job.download_link)
                if response.code >= 200 and response.code < 300:
                    job.done(response.read())
                    print "Download complete"
                    self.file_queue.put(job)
            except:
                if job.count < 3:
                    print "Download failed, retrying"
                    self.failed_queue.put(job)
            finally:
                self.url_queue.task_done()


class FileSaveThread(threading.Thread):

    def __init__(self, file_queue, update_queue):
        threading.Thread.__init__(self)
        self.file_queue = file_queue
        self.update_queue = update_queue

    def run(self):
        while True:
            job = self.file_queue.get()
            with open(job.file_name, 'wb') as f:
                f.write(job.content)
                print "File %s saved" % job.file_name
            self.update_queue.put(job)
            self.file_queue.task_done()


class UpdatePageThread(threading.Thread):

    def __init__(self, update_queue):
        threading.Thread.__init__(self)
        self.update_queue = update_queue

    def run(self):
        while True:
            job = self.update_queue.get()
            page = session.query(Page).filter(Page.id == job.page_id).first()
            page.downloaded = True
            session.add(page)
            session.commit()
            print "Page [%d] saved" % page.id
            self.update_queue.task_done()


class RetryThread(threading.Thread):

    def __init__(self, url_queue, failed_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.failed_queue = failed_queue

    def run(self):
        while True:
            job = self.failed_queue.get()
            self.url_queue.put(job)
            self.failed_queue.task_done()
