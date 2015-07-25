from bs4 import BeautifulSoup as bs
import requests


site = 'http://adrenaline.uol.com.br/forum/sale-221'
base_url = 'http://adrenaline.uol.com.br/forum'
html_doc = requests.get(site)
soup = bs(html_doc.content)

# print(soup.prettify().encode('utf-8'))

import urllib
import lxml.html

def complete_links(partial_url, base_url):
    return '{}/{}'.format(base_url, partial_url)

def get_thread_links(scrape_url, base_url, n_links = 5):
    links_list = set()
    links_count = 0
    connection = urllib.urlopen(scrape_url)
    dom =  lxml.html.fromstring(connection.read())
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        if 'showthread' in link:
            link, _ = link.split('&', 1)
            links_list.add(complete_links(link, base_url))
            links_count += 1
        if len(links_list) == n_links:
           return links_list





links = get_thread_links(site, base_url, 10)


for thread in links:
    html_doc = requests.get(thread)
    soup = bs(html_doc.content)
    print(soup.title.encode('utf-8'))