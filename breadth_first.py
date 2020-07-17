from bs4 import BeautifulSoup
from urllib.request import urlparse, urljoin
import requests
import time
from threading import Lock, Thread
from queue import Queue
import sys

# var that checks if we've visited this before
internal_urls = set()
page_queue = Queue()
MAX_STEPS = 10
global MASTER_COMPLETE
MASTER_COMPLETE = False

def worker():
    item = page_queue.get()
    if not MASTER_COMPLETE:
        wikipedia_game(item[0],item[1],item[2],item[3])
    page_queue.task_done()



# start and end are both urls
def wikipedia_game(start, end, path, steps):
    # exit condition here
    global MASTER_COMPLETE
    if MASTER_COMPLETE:
        return
    
    links = get_all_website_links(start)
    if end in links:
        print(path + ' ->\n' + end)
        MASTER_COMPLETE = True
        return path + ' ->\n' + end
    
    elif len(links) == 0 or steps > MAX_STEPS:
    #elif len(links) == 0:
        #print(path, 'all visited links')
        return None
    else:
        for link in links:
            page_queue.put([link , end , path + ' ->\n' + link, steps+1])


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            # if href not in external_urls:
            #     print(f"{GRAY}[!] External link: {href}{RESET}")
            #     external_urls.add(href)
            continue
        #print('Internal link: '+href)
        urls.add(href)
        internal_urls.add(href)
    return urls

s = 'https://en.wikipedia.org/wiki/Dark_Souls'

e = 'https://en.wikipedia.org/wiki/Fish_finger'

page_queue.put([s,e,s,0])
start_time = time.time()
while not MASTER_COMPLETE:
    # while not page_queue.empty():
        Thread(target=worker, daemon=True).start()

print(time.time() - start_time, 'Seconds')
    

