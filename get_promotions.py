from bs4 import BeautifulSoup as bs
import requests
import urllib
import lxml.html


site = 'http://adrenaline.uol.com.br/forum/sale-221'
base_url = 'http://adrenaline.uol.com.br/forum'
html_doc = requests.get(site)
soup = bs(html_doc.content)


def get_title(url):
    html_doc = requests.get(url)
    soup = bs(html_doc.content)
    return soup.title.encode('utf-8')


def complete_links(partial_url, base_url):
    return '{}/{}'.format(base_url, partial_url)


def get_thread_links(scrape_url, base_url, key_word, n_links=25):
    '''Key_word argument to filter the threads of a given forum'''
    links_list = set()
    connection = urllib.urlopen(scrape_url)
    dom = lxml.html.fromstring(connection.read())
    for link in dom.xpath('//a/@href'):
        if key_word in link:
            link, _ = link.split('&', 1)
            links_list.add(complete_links(link, base_url))
        if len(links_list) == n_links:
            return links_list
            # yield complete_links(link, base_url)



links = get_thread_links(site, base_url, 'showthread')

for link in links:
    title = get_title(link)
    _, thread_title = title.strip().split('>', 1)
    if thread_title.startswith('['):
        print(thread_title)


# n_links = 0

# while n_links < 3:
#     thread_title = get_title(next(links))
#     # if thread_title.startswith('['):
#     # print (thread_title)
#     _, title = thread_title.split('>', 1)
#     if title.strip().startswith('['):
#         print(title)
#     n_links += 1
