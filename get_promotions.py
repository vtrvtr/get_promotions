import lxml.html
import os
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


FILE_PATH = 'E:\\Documents\\promocoes.txt'
time = datetime.now()


def get_html_cloudfare(link):
    scraper = cfscrape.create_scraper()
    return scraper.get(link).content


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
    _, t = link.rsplit('/', 1)
    thread_title, _ = t.split('.')
    formatted_title = ' '.join([word for word in thread_title.split('-')])
    return "\nPromo: {}\nLink: {}\n".format(formatted_title.replace(' r ', ' R$').title(), link)


def format_hardmob_links(link):
    _, title = link.split('-', 1)
    c, _ = title.split('.', 1)
    formatted_title = ' '.join(
        [word for word in c.split('-')[1:] if word is not '-'])
    return "\nPromo: {}\nLink: {}\n".format(formatted_title.replace(' r ', ' R$').title(), link)


def gen_adrenaline_links(scrap_url='http://adrenaline.uol.com.br/forum/forums/for-sale.221/', base_url='http://adrenaline.uol.com.br/forum', key_word='thread', n_links=10):
    '''Key_word argument to filter the threads of a given forum'''
    dom = get_soup(scrap_url)
    links_list = set()
    for link in dom.findAll('a'):
        href = link.get('href')
        if href:
            if key_word in href and not any(word in href for word in['atencao', 'regras', 'censurados']):
                link, _ = href.rsplit('/', 1)
                links_list.add(complete_links(link, base_url))
            elif len(links_list) == n_links:
                break
    for link in set(links_list):
        corrected_link = format_adrenaline_link(link)
        if corrected_link:
            yield corrected_link


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


def gen_promoforum_links(scrap_url='http://www.promoforum.com.br/forums/promocoes', n_links=5):
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
                yield format_hardmob_links(complete_links(thread_link, base_link))
                link_count += 1
            if link_count == n_links:
                break

def gen_promobit_links(scrap_url='http://www.promobit.com.br/Promocoes/em-destaque/page/1-2', n_links=5):
    soup = get_soup(scrap_url)
    base_link = 'http://www.promobit.com.br'
    for link in soup.findAll('a'):
        try:
            href = link.get('href').encode('utf-8')
            info = link.text.encode('utf-8')
            if 'ver-promocoes' in href and 'R$' in info:
                title, price = link.text.encode('utf-8').split('R$', 1)
                formatted_title = "\nPromo: {} por R${}Link: {}{}\n".format(
                    title.strip(), price.rsplit(' ', 1)[1], base_link, href)
                yield formatted_title
        except AttributeError:
            continue

def check_link_presence(promotion, path=FILE_PATH):
    with open(path) as f:
        text = f.read()
        return True if promotion in text else False

def populate_txt(links):
    '''checks if link is already on file
    links (generator/list) -> txt wrote'''
    for link in links:
        if not check_link_presence(link):
            with open(FILE_PATH, 'a+') as f:
                f.write(link)


def main():
    with open(FILE_PATH, 'r+') as f:
        old_text = f.read()
        f.seek(0)
        f.truncate()
    populate_txt(gen_promobit_links(n_links=2))
    populate_txt(gen_adrenaline_links(n_links=2))
    populate_txt(gen_promoforum_links(n_links=2))
    with open(FILE_PATH, 'r') as g:
        new_text = g.read()
    print(new_text == old_text)
    if new_text != old_text:
        os.startfile(FILE_PATH)

if __name__ == '__main__':
    main()
