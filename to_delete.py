import requests
from bs4 import BeautifulSoup


# print "Searching for " + movie_name

moviesearch_link = requests.get("https://thepiratebay.vg/search/" + 'kingsman' + "/0/99/0")

convert_moviesearch_link = moviesearch_link.text

soup = BeautifulSoup(convert_moviesearch_link, "lxml")

magnet_links = soup.find_all(title='Download this torrent using magnet')

def find_link():
    for link in magnet_links[:1]:
        link = str(link)
        print(link)
        if 'xvid-etrg' in link.lower():
            link = link[9:-121]
            print link
            # webbrowser.open(link)

find_link()