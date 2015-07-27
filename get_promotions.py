from bs4 import BeautifulSoup as bs
import requests
import urllib
import lxml.html
import cProfile

'''format:
scrap_url, base_url, key_word (if needed)'''

sites = {'adrenaline': [
    'http://adrenaline.uol.com.br/forum/sale-221', 'http://adrenaline.uol.com.br/forum', 'showthread'], 'hardmob': ['http://www.hardmob.com.br/promocoes', 'http://www.hardmob.com.br/promocoes', 'promocoes']}

def get_title(url):
    html_doc = requests.get(url)
    soup = bs(html_doc.content)
    return soup.title.encode('utf-8')


def complete_links(partial_url, base_url):
    return '{}/{}'.format(base_url, partial_url)


def get_dom(scrap_url):
    html_doc = requests.get(scrap_url)
    return lxml.html.fromstring(html_doc.content)

def get_soup(link):
    html_doc = requests.get(link)
    return bs(html_doc.content)


def format_adrenaline_link(link):
    title = get_title(link)
    _, t = title.split('>', 1)
    thread_title, _ = t.split('<', 1)
    return "Promo: {}\nLink: {}".format(thread_title, link) if thread_title.startswith(' [') else None


def get_adrenaline_links(scrap_url='http://adrenaline.uol.com.br/forum/sale-221', base_url='http://adrenaline.uol.com.br/forum', key_word='showthread', n_links=10):
    '''Key_word argument to filter the threads of a given forum'''
    dom = get_dom(scrap_url)
    links_list = set()
    for link in dom.xpath('//a/@href'):
        if key_word in link:
            link, _ = link.split('&', 1)
            links_list.add(complete_links(link, base_url))
        if len(links_list) == n_links:
            break
    for link in links_list:
        corrected_link = format_adrenaline_link(link)
        if corrected_link:
            print(corrected_link)

def format_hardmob_links(link):
    _, title = link.split('-', 1)
    c, _ = title.split('.', 1)
    formatted_title = ' '.join([word for word in c.split('-')[1:] if word is not '-'])
    # print formatted_title.replace(' r ', ' R$')
    return "Promo: {}\nLink: {}".format(formatted_title.replace(' r ', ' R$').title(), link) 

def get_hardmob_links(scrap_url = 'http://www.hardmob.com.br/promocoes', n_links = 10):
    dom = get_soup(scrap_url)
    link_count = 0
    for link in dom.findAll('a'):
        if link.get('id'):
            if 'thread_title' in link.get('id') and 'twitter' not in link.get('href') and 'faq' not in link.get('href'):
                thread_link = link.get('href')
                print(format_hardmob_links(thread_link))
                link_count += 1
            if link_count == n_links:
                break

get_hardmob_links()

print 'twitter' not in 'http://www.hardmob.com.br/promocoes/449293-twitter-siga-a-hardmob-promocoes-status-ok.html'


