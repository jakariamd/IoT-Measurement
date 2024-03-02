from fuzzywuzzy import fuzz
from string import digits
import ast
import whois


# get org name from python whois


def get_org_python_whois(sld):
    print(sld, ': ', end='')
    try:
        who = whois.whois(sld)
        org = who['org']
        print(org)
    except:
        org = None
        print(None)
    return org


def check_privacy_mask(org_name, privacy_masks):
    if (org_name is None) or (type(org_name) is not str):
        return False

    for mask in privacy_masks['masks']:
        if fuzz.ratio(org_name.lower().translate(str.maketrans('', '', digits)),
                      mask.lower().translate(str.maketrans('', '', digits))) > 90:
            return True
    return False


def clean_multiple_org(org_name):
    if type(org_name) is str and org_name.startswith('['):
        org_name = ast.literal_eval(org_name)
        return org_name[0]
    return org_name


# Crawl Netify for org information
import requests
import urllib
from requests_html import HTMLSession
import random

googleTrendsUrl = 'https://www.netify.ai'
response = requests.get(googleTrendsUrl)
if response.status_code == 200:
    g_cookies = response.cookies.get_dict()

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36']

http_proxy = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy = "ftp://10.10.1.10:3128"

proxies = {
    "http": http_proxy,
    "https": https_proxy,
    "ftp": ftp_proxy
}


def get_source(url):
    """Return the source code for the provided URL.
    Args:
        url (string): URL of the page to scrape.
    Returns:
        response (object): HTTP response object from requests_html.
    """
    try:
        # sleep(random.randint(1,2))
        headers = {'User-Agent': random.choice(user_agent_list)}
        session = HTMLSession()
        response = session.get(url, headers=headers, cookies=g_cookies)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def parse_results(response):
    if response.status_code == 404:
        return None

    css_identifier_text = '.col-md-7'
    try:
        text = response.html.find(css_identifier_text, first=True).text.split('\n')
        org_name = text[0].split(' - ')[0]
        service_name = text[0].split(' - ')[1]
        service_description = text[1]
        output = [org_name, service_name, service_description]
    except:
        output = None

    return output


def netify_search(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.netify.ai/resources/domains/" + query)
    return parse_results(response)


# Selenium Copyright Crawler


import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import translators as ts
from langdetect import detect
from selenium import webdriver

import en_core_web_lg
import en_core_web_md

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

nlp = en_core_web_lg.load()
md_nlp = en_core_web_md.load()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(10)


def selenium_request(url):
    driver.get(url)
    return driver.page_source


# driver.quit()
# Define a class that returns copyright information

class Copyright_Crawler:

    def __init__(self, domain):
        self.domain = domain
        self.copyright_first_index = []
        self.copyright_last_index = []
        self.copyright_default = []

    def get_copyrights(self, soup):
        copyright = soup.findAll(lambda tag: re.search(r"©|[Cc][Oo][Pp][Yy][Rr][Ii][Gg][Hh][Tt]", tag.text))
        copyright_first_index = ''
        copyright_last_index = ''
        copyright_default = ''

        try:
            copyright_first_index = copyright[0].text
            for X in nlp(copyright_first_index).ents:
                if X.label_ == 'ORG':
                    self.copyright_first_index.append(X.text)
        except:
            None

        try:
            if len(copyright) == 1:
                self.copyright_last_index = self.copyright_first_index
            else:
                copyright_last_index = copyright[-1].text
                for X in nlp(copyright_last_index).ents:
                    if X.label_ == 'ORG':
                        self.copyright_last_index.append(X.text)

                if len(self.copyright_last_index) == 0:
                    for X in nlp(copyright_last_index).ents:
                        if X.label_ == 'ORG':
                            self.copyright_last_index.append(X.text)
        except:
            None

        try:
            if (len(copyright_last_index) == 0) and (len(copyright_first_index) != 0):
                self.copyright_default = self.copyright_first_index

            elif (len(copyright_last_index) != 0) and (len(copyright_first_index) == 0):
                self.copyright_default = self.copyright_last_index

            elif len(copyright_first_index) < len(copyright_last_index):
                self.copyright_default = self.copyright_first_index
            else:
                self.copyright_default = self.copyright_last_index

            if len(self.copyright_default) == 0:
                if len(self.copyright_first_index) != 0:
                    self.copyright_default = self.copyright_first_index
                elif len(self.copyright_last_index) != 0:
                    self.copyright_default = self.copyright_last_index
        except:
            None

    def get_copyrights_not_en(self, soup):
        copyright = soup.findAll(lambda tag: re.search(r"©|[Cc][Oo][Pp][Yy][Rr][Ii][Gg][Hh][Tt]", tag.text))
        copyright_first_index = ''
        copyright_last_index = ''
        copyright_default = ''

        try:
            if len(copyright[0].text) < 5000:
                copyright_first_index = ts.google(copyright[0].text)
            else:
                lines = re.findall(r"^.*©.*$", copyright[0].text, re.MULTILINE)
                copyright_first_index = ts.google(' '.join(lines))

            for X in nlp(copyright_first_index).ents:
                if X.label_ == 'ORG':
                    self.copyright_first_index.append(X.text)
        except:
            None

        try:
            if len(copyright) == 1:
                self.copyright_last_index = self.copyright_first_index
            else:
                copyright_last_index = ts.google(copyright[-1].text)
                for X in nlp(copyright_last_index).ents:
                    if X.label_ == 'ORG':
                        self.copyright_last_index.append(X.text)
        except:
            None

        try:
            if (len(copyright_last_index) == 0) and (len(copyright_first_index) != 0):
                self.copyright_default = self.copyright_first_index

            elif (len(copyright_last_index) != 0) and (len(copyright_first_index) == 0):
                self.copyright_default = self.copyright_last_index

            elif len(copyright_first_index) < len(copyright_last_index):
                self.copyright_default = self.copyright_first_index
            else:
                self.copyright_default = self.copyright_last_index

            if len(self.copyright_default) == 0:
                if len(self.copyright_first_index) != 0:
                    self.copyright_default = self.copyright_first_index
                elif len(self.copyright_last_index) != 0:
                    self.copyright_default = self.copyright_last_index
        except:
            None

    def crawl_selenium(self, url):
        try:
            html = selenium_request('http://' + url)
        except:
            html = None

        if html is None:
            try:
                html = selenium_request('http://www.' + url)
            except:
                return None

        soup = BeautifulSoup(html, 'lxml')

        try:
            title = soup.find("title").get_text()
        except:
            title = None

        if (title is None) or (detect(title) == 'en'):
            self.get_copyrights(soup)

        else:
            self.get_copyrights_not_en(soup)
            if len(self.copyright_default) == 0:
                self.crawl_selenium_not_en(self.domain)

    def crawl(self, url):
        try:
            html = requests.get('http://' + url, timeout=(2, 3)).text
        except:
            html = None

        if html is None:
            try:
                html = requests.get('http://www.' + url, timeout=(2, 3)).text
            except:
                return None

        soup = BeautifulSoup(html, 'lxml')

        try:
            title = soup.find("title").get_text()
        except:
            title = None

        try:
            page_language = detect(title)
        except:
            page_language = 'en'

        if (title is None) or (page_language == 'en'):
            self.get_copyrights(soup)
            if len(self.copyright_default) == 0:
                self.crawl_selenium(self.domain)
        else:
            self.get_copyrights_not_en(soup)
            if len(self.copyright_default) == 0:
                self.crawl_not_en(self.domain)

                if len(self.copyright_default) == 0:
                    self.crawl_selenium(self.domain)

    def crawl_not_en(self, url):
        url_replcaed = url.replace('.', '-')
        try:
            html = requests.get(
                'https://' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp',
                timeout=5).text
        except:
            html = None

        if html is None:
            try:
                html = requests.get(
                    'https://www-' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp',
                    timeout=5).text
            except:
                return None

        if html is None:
            try:
                url_replcaed = url_replcaed.replace('-net', '-com')
                html = requests.get(
                    'https://' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp',
                    timeout=5).text
            except:
                return None

        if html is None:
            try:
                url_replcaed = url_replcaed.replace('-net', '-com')
                html = requests.get(
                    'https://www-' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp',
                    timeout=5).text
            except:
                return None
        soup = BeautifulSoup(html, 'lxml')
        self.get_copyrights(soup)

    def crawl_selenium_not_en(self, url):
        url_replcaed = url.replace('.', '-')
        try:
            html = selenium_request(
                'https://' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp')
        except:
            html = None

        if html is None:
            try:
                html = selenium_request(
                    'https://www-' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp')
            except:
                return None

        if html is None:
            try:
                url_replcaed = url_replcaed.replace('-net', '-com')
                html = selenium_request(
                    'https://' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp')
            except:
                return None

        if html is None:
            try:
                url_replcaed = url_replcaed.replace('-net', '-com')
                html = selenium_request(
                    'https://www-' + url_replcaed + '.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp')
            except:
                return None
        soup = BeautifulSoup(html, 'lxml')
        self.get_copyrights(soup)

    def unique(self):
        self.copyright_first_index = list(np.unique(np.array(self.copyright_first_index)))
        self.copyright_last_index = list(np.unique(np.array(self.copyright_last_index)))
        self.copyright_default = list(np.unique(np.array(self.copyright_default)))

    def run(self):
        # logging.info(f'Crawling: {self.domain}')
        try:
            self.crawl(self.domain)
        except Exception:
            logging.exception(f'Failed to crawl: {self.domain}')
        finally:
            self.unique()
            return self.copyright_first_index, self.copyright_last_index, self.copyright_default


# Test
# Copyright_Crawler(domain='verizon.net').run()
# Copyright_Crawler(domain='sleepnumber.com').run()
# Copyright_Crawler(domain='https://fastly-net.translate.goog?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp').run()


# Web Scrapper
# Define a class that returns useful Privacy Policy/Contact US links

def request_html(url):
    try:
        html = selenium_request('https://' + url)
        # html = requests.get('http://' + url, timeout= 10).text
        url = 'http://' + url
        return html, url
    except:
        None

    try:
        html = requests.get('https://' + url, timeout=5).text
        url = 'https://' + url
        return html, url
    except:
        None

    try:
        html = requests.get('https://www.' + url, timeout=5).text
        url = 'https://www.' + url
        return html, url
    except:
        None

    try:
        html = requests.get('http://www.' + url, timeout=5).text
        url = 'http://www.' + url
        return html, url
    except:
        return None, None


class Crawler:

    def __init__(self, domain):
        self.urls_to_scrap = []
        self.domain = domain
        self.language = True

    def get_linked_urls(self, url, soup):
        for link in soup.find_all('a', href=True, text=re.compile(
                r'[Pp][Rr][Ii][Vv][Aa][Cc][Yy]|[Aa][Bb][Oo][Uu][Tt]|[Cc][Oo][Nn][Tt][Aa][Cc][Tt]|[Tt][Ee][Rr][Mm]|[Pp][Oo][Ll][Ii][Cc][Yy]')):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            elif path and path.startswith('./'):
                path = urljoin(url, path[1:])
            elif path and (not path.startswith('http')):
                path = urljoin(url, '/' + path)
            yield path

    def get_linked_urls_not_en(self, url, soup):
        for link in soup.findAll('a'):
            if link.string and (len(link.string) < 500):
                try:
                    link.string.replace_with(ts.google(link.string))
                except:
                    None
            elif link.string and (len(link.string) > 500):
                try:
                    link.string.replace_with(ts.google((link.string)[:500]))
                except:
                    None

        for link in soup.find_all('a', href=True, text=re.compile(
                r'[Pp][Rr][Ii][Vv][Aa][Cc][Yy]|[Aa][Bb][Oo][Uu][Tt]|[Cc][Oo][Nn][Tt][Aa][Cc][Tt]|[Tt][Ee][Rr][Mm]|[Pp][Oo][Ll][Ii][Cc][Yy]')):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            elif path and path.startswith('./'):
                path = urljoin(url, path[1:])
            elif path and (not path.startswith('http')):
                path = urljoin(url, '/' + path)
            yield path

    def crawl(self, url):
        html, url = request_html(url)
        if html is None:
            return None

        soup = BeautifulSoup(html, 'html.parser')

        try:
            title = detect(soup.find("title").get_text())
        except:
            title = None

        try:
            lang = soup.html.attrs['lang']
        except:
            lang = None

        if (lang is not None) and ('en' in lang):
            linked_urls = self.get_linked_urls(url, soup)
        elif (lang is not None) and ('en' not in lang):
            self.language = False
            linked_urls = self.get_linked_urls_not_en(url, soup)
        elif (title is not None) and (title == 'en'):
            linked_urls = self.get_linked_urls(url, soup)
        else:
            self.language = False
            linked_urls = self.get_linked_urls_not_en(url, soup)

        for link in linked_urls:
            if link not in self.urls_to_scrap:
                self.urls_to_scrap.append(link)

    def run(self):
        try:
            self.crawl(self.domain)
        except Exception:
            logging.exception(f'Failed to crawl: {self.domain}')
        finally:
            return self.urls_to_scrap, self.language


# TEST
# start = timer()
# print(Crawler(domain='tplinkcloud.com').run())
# end = timer()
# print(end - start)

# Define a class that returns organization name by scraping Privacy Policy/Contact US links Links
# This scraper extract organization name from all the paragraphs of a web page.

class Scraper:

    def __init__(self, urls, language):
        self.urls_to_scrap = urls
        self.language = language
        self.organization_list = []

    def scrap(self, url):
        try:
            html = requests.get(url, timeout=10).text
            # html = selenium_reques(url)
        except:
            return None

        soup = BeautifulSoup(html, 'html.parser')

        if (self.language):
            self.scrap_orgs_en(soup)
        else:
            self.scrap_orgs_not_en(soup)

    def scrap_orgs_en(self, soup):
        org_in_this_url = []
        try:
            text = " ".join(soup.text.split())[:4999]
            ents = nlp(text).ents
        except:
            ents = []

        for X in ents:
            if len(org_in_this_url) >= 5:
                break
            if X.label_ == 'ORG':
                org_in_this_url.append(X.text)
        self.organization_list.extend(org_in_this_url)

    def scrap_orgs_not_en(self, soup):
        org_in_this_url = []

        try:
            text = " ".join(soup.text.split())[:4999]
            ents = nlp(ts.google(text)).ents
        except:
            ents = []

        for X in ents:
            if len(org_in_this_url) >= 5:
                break
            if X.label_ == 'ORG':
                org_in_this_url.append(X.text)

        self.organization_list.extend(org_in_this_url)

    def run(self):
        for url in self.urls_to_scrap:
            self.scrap(url)
        return list(dict.fromkeys(self.organization_list))

# TEST
# start = timer()
# urls, language = Crawler(domain='svt.se').run()
# print(urls)
# print(Scraper(urls, language).run())
# print(Scraper(urls=['http://xs4all.nl/contact/', 'http://xs4all.nl/klant/welcome-to-xs4all/',
# 'http://xs4all.nl/contact/#contact', 'http://xs4all.nl/klant/voorwaarden/', 'http://xs4all.nl/klant/privacy/'],
# language=False).run())
# end = timer()
# print(end - start)
