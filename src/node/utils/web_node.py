# import requests
import re
from bs4 import BeautifulSoup
import urllib.request
import requests


# http://www.cubaeduca.cu
# http://www.etecsa.cu
# http://www.uci.cu
# http://evea.uh.cu
# http://www.uo.edu.cu
# lento: http://www.uclv.edu.cu
# http://covid19cubadata.uh.cu
# http://www.uh.cu


class WebNode:
    def __init__(self, url: str) -> None:
        self.url = url
        self.html = None
        self.level_one_links = []
        self.level_one_html = []
        self.level_two_links = []
        self.level_two_html = []
        try:
            _, self.domain = url.split('://www.')
        except:
            try:
                _, self.domain = url.split('://')
            except:
                self.domain = url



        self.scrap()
        self.print_web_links()

    def scrap(self):
        try:
            self.html = urllib.request.urlopen(self.url).read()
        except Exception as e:
            self.html = e
            print(e)
            return

        print(self.url)
        # print(self.html)

        self.level_one_links = self.find_links_in_html(self.html)
        self.level_one_html = self.get_html_list(self.level_one_links)


        for html in self.level_one_html:
            self.level_two_links = self.find_links_in_html(html)
            self.level_two_html = self.get_html_list(self.level_two_links)


    def find_links_in_html(self, html):
        soup = BeautifulSoup(html, features="lxml")
        links = soup.findAll('a', href=True)
        res = []

        for link in links:
            link = link['href']
            print(link)
            if link in self.level_one_links or link in self.level_two_links:
                continue
            belongs_to_domain = re.search(self.domain, link)
            if belongs_to_domain:
                res.append(link)
        return res


    def get_html_list(self, links:list):
        html_list = []
        for link in links:
            try:
                html_list.append(urllib.request.urlopen(link).read())
            except Exception as e:
                html_list.append(e)
        return html_list

    def print_web_links(self):
        print(self.url)
        print('LEVEL ONE', *self.level_one_links, sep="\n")
        print('LEVEL TWO', *self.level_two_links, sep='\n')

web_node = WebNode('http://www.cubaeduca.cu')

# html = urllib.request.urlopen('https://www.google.es/').read()

print('fin')