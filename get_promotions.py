from bs4 import BeautifulSoup as bs
import requests
import urllib
import lxml.html
import cProfile

'''format:
scrap_url, base_url, key_word'''

sites = {'adrenaline': [
    'http://adrenaline.uol.com.br/forum/sale-221', 'http://adrenaline.uol.com.br/forum', 'showthread']}
# html_doc = requests.get(site)
# soup = bs(html_doc.content)


def get_title(url):
    html_doc = requests.get(url)
    soup = bs(html_doc.content)
    return soup.title.encode('utf-8')


def complete_links(partial_url, base_url):
    return '{}/{}'.format(base_url, partial_url)


def get_thread_links(scrap_url, base_url, key_word, n_links=10):
    '''Key_word argument to filter the threads of a given forum'''
    connection = urllib.urlopen(scrap_url)
    dom = lxml.html.fromstring(connection.read())
    links_list = set()
    for link in dom.xpath('//a/@href'):
        if key_word in link:
            link, _ = link.split('&', 1)
            links_list.add(complete_links(link, base_url))
        if len(links_list) == n_links:
            return links_list


def filter_adrenaline(scrap_url, base_url, key_word):
    formatted_links = []
    for link in get_thread_links(scrap_url, base_url, key_word):
        title = get_title(link)
        _, t = title.split('>', 1)
        thread_title, _ = t.split('<', 1)
        print(thread_title)
        if thread_title.startswith('aaa ['):
            print("Promo: {} \n Link: {}".format(thread_title, link).encode('utf-8'))
    return formatted_links


filter_adrenaline(
    sites['adrenaline'][0], sites['adrenaline'][1], sites['adrenaline'][2])

# while n_links < 3:
#     thread_title = get_title(next(links))
# if thread_title.startswith('['):
# print (thread_title)
#     _, title = thread_title.split('>', 1)
#     if title.strip().startswith('['):
#         print(title)
#     n_links += 1
