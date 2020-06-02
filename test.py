from bs4 import BeautifulSoup
from urllib.request import urlparse, urljoin
import requests
import time

# var that checks if we've visited this before
internal_urls = set()

MAX_STEPS = 10

# start and end are both urls
def wikipedia_game(start, end, path,steps):
    
    links = get_all_website_links(start)
    if end in links:
        return path + ' ->\n' + end
    
    elif len(links) == 0 or steps > MAX_STEPS:
    #elif len(links) == 0:
        #print(path, 'all visited links')
        return None
    else:
        for link in links:
            response = wikipedia_game(link, end, path + ' ->\n'+ link, steps+1)
            if response:
                return response


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

s = 'https://en.wikipedia.org/wiki/NASA'

e = 'https://en.wikipedia.org/wiki/Coronavirus_disease_2019'


start_time = time.time()
for steps in range(3,8):
    MAX_STEPS = steps
    print('Max Steps:', steps)
    print(wikipedia_game(s,e,s,0))
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n')
    internal_urls = set()
