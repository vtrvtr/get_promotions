import lxml.html
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from subprocess import Popen

FILE_PATH = 'E:\\Documents\\promocoes.txt'
FILE = open(FILE_PATH, 'w')
time = datetime.now()


def get_title(soup):
    return soup.title.encode('utf-8')


def complete_links(partial_url, base_url):
    return '{}/{}'.format(base_url, partial_url)


def get_dom(scrap_url):
    '''html_link -> lxml dom'''
    html_doc = requests.get(scrap_url)
    return lxml.html.fromstring(html_doc.content)


def get_soup(link):
    '''html link -> BeautifulSoup soup'''
    html_doc = requests.get(link)
    return bs(html_doc.content)


def format_adrenaline_link(link):
    '''link (adrenaline) -> formatted link
    '''
    title = get_title(get_soup(link))
    _, title = title.split('>', 1)
    thread_title, _ = title.split('<', 1)
    return "\nPromo: {}\nLink: {}\n".format(thread_title, link) if thread_title.startswith(' [') else None


def format_hardmob_links(link):
    _, title = link.split('-', 1)
    c, _ = title.split('.', 1)
    formatted_title = ' '.join(
        [word for word in c.split('-')[1:] if word is not '-'])
    return "\nPromo: {}\nLink: {}\n".format(formatted_title.replace(' r ', ' R$').title(), link)


def get_adrenaline_links(scrap_url='http://adrenaline.uol.com.br/forum/sale-221', base_url='http://adrenaline.uol.com.br/forum', key_word='showthread', n_links=10):
    '''Key_word argument to filter the threads of a given forum'''
    dom = get_soup(scrap_url)
    links_list = set()
    # for link in dom.xpath('//a/@href'):
    for link in dom.findAll('a'):
        href = link.get('href')
        if href:
            if key_word in href:
                link, _ = href.split('&', 1)
                links_list.add(complete_links(link, base_url))
            if len(links_list) == n_links:
                break
    for link in links_list:
        corrected_link = format_adrenaline_link(link)
        if corrected_link:
            try:
                FILE.write(corrected_link)
            except Exception as e:
                FILE.write(e)


def get_hardmob_links(scrap_url='http://www.hardmob.com.br/promocoes', n_links=5):
    dom = get_soup(scrap_url)
    link_count = 0
    for link in dom.findAll('a'):
        if link.get('id'):
            if 'thread_title' in link.get('id') and 'twitter' not in link.get('href') and 'faq' not in link.get('href') and 'descontos' not in link.get('href'):
                thread_link = link.get('href')
                try:
                    FILE.write(format_hardmob_links(thread_link))
                except Exception as e:
                    FILE.write(e)
                link_count += 1
            if link_count == n_links:
                break


def get_promoforum_links(scrap_url='http://www.promoforum.com.br/forums/promocoes', n_links=5):
    '''
    I'm using the hardmob format here just because it fits perfectly
    '''
    base_link = 'http://www.promoforum.com.br/'
    dom = get_soup(scrap_url)
    link_count = 0
    for link in dom.findAll('a'):
        if link.get('class'):
            if link.get('class')[0] == 'PreviewTooltip' and 'postar' not in link.get('href'):
                thread_link = link.get('href')
                try:
                    FILE.write(
                        format_hardmob_links(complete_links(thread_link, base_link)))
                except Exception as e:
                    FILE.write(e)
                link_count += 1
            if link_count == n_links:
                break


def main():
    FILE.write('Last update: {}'.format(time))
    get_adrenaline_links()
    get_hardmob_links()
    get_promoforum_links()

if __name__ == '__main__':
    main()
