import os
import re
import requests
import threading
from urlparse import urlparse, urljoin
from BeautifulSoup import BeautifulSoup

class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class ImageDownloaderThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print "Starting thread ", self.name
        download_images(self.name)
        print "Finished thread ", self.name

def traverse_site(max_links=10):
    link_parser_singleton = Singleton()
    while link_parser_singleton.queue_to_parse:
        if len(link_parser_singleton.to_visit) == max_links:
            return
        url = link_parser_singleton.queue_to_parse.pop()
        try:
            response = requests.get(url)
        except Exception:
            continue
        if response.headers["content-type"] != "text/html; charset=utf-8":
            continue
        link_parser_singleton.to_visit.add(url)
        print "Added", url, "to queue"
        bs = BeautifulSoup(response.text)
        for link in BeautifulSoup.findAll(bs, "a"):
            link_url = link.get("href")
            if not link_url:
                continue
            parsed = urlparse(link_url)
            if parsed.netloc and parsed.netloc != parsed_root.netloc:
                continue
            link_url = (parsed.scheme or parsed_root.scheme) + "://" + \
                (parsed.netloc or parsed_root.netloc) + parsed.path or ""
            if link_url in link_parser_singleton.to_visit:
                continue
            link_parser_singleton.queue_to_parse = [link_url] + \
                link_parser_singleton.queue_to_parse

def download_images(thread_name):
    singleton = Singleton()
    while singleton.to_visit:
        url = singleton.to_visit.pop()
        print "Start downloading images from", url
        try:
            response = requests.get(url)
        except Exception:
            continue
        bs = BeautifulSoup(response.text)
        images = BeautifulSoup.findAll(bs, "img")
        for image in images:
            src = image.get("src")
            src = urljoin(url, src)
            basename = os.path.basename(src)
            if src not in singleton.downloaded:
                singleton.downloaded.add(src)
                print "Downloading", src
                with open(os.path.join("images", basename), "wb") as f:
                    response = requests.get(src)
                    f.write(response.content)
        print thread_name, "finished downloading images from", url

if __name__ == "__main__":
    root = "http://moeabdol.com"
    parsed_root = urlparse(root)
    singleton = Singleton()
    singleton.queue_to_parse = [root]
    singleton.to_visit = set()
    singleton.downloaded = set()
    traverse_site()
    if not os.path.exists("images"):
        os.makedirs("images")

    thread1 = ImageDownloaderThread(1, "Thread-1", 1)
    thread2 = ImageDownloaderThread(2, "Thread-2", 2)
    thread1.start()
    thread2.start()
