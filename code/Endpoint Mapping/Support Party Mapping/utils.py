import requests
import urllib
from requests_html import HTMLSession
import random

googleTrendsUrl = 'https://google.com'
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
        headers = {'User-Agent': random.choice(user_agent_list)}
        session = HTMLSession()
        response = session.get(url, headers=headers, cookies=g_cookies)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def get_results_google(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    # response = get_source("https://www.google.co.uk/search?q=" + query)
    return response


def parse_results_google(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:

        try:
            item = {
                'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).attrs['href'],
                'text': result.find(css_identifier_text, first=True).text
            }
            output.append(item)
        except:
            None

    return output


def google_search(query):
    response = get_results_google(query)
    return parse_results_google(response)


def get_results_bing(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.bing.com/search?q=" + query)
    return response


def parse_results_bing(response):
    output = []

    try:
        css_identifier_title = '.b_focusTextMedium'
        css_identifier_link = '.df_con a'
        css_identifier_text = '.df_con'

        item = {
            'title': response.html.find(css_identifier_title, first=True).text,
            'link': response.html.find(css_identifier_link, first=True).attrs['href'],
            'text': response.html.find(css_identifier_text, first=True).text
        }
        output.append(item)
    except:
        None

    try:
        css_identifier_text = '.b_ans .rwrl'
        css_identifier_title = '.b_ans .b_algo'
        css_identifier_link = '.b_ans .b_algo a'

        item = {
            'title': response.html.find(css_identifier_title, first=True).text,
            'link': response.html.find(css_identifier_link, first=True).attrs['href'],
            'text': response.html.find(css_identifier_text, first=True).text
        }
        output.append(item)
    except:
        None

    css_identifier_result = ".b_algo"

    css_identifier_title = "h2"
    css_identifier_link = ".b_caption .b_attribution cite"
    css_identifier_text = ".b_caption p"

    results = response.html.find(css_identifier_result)
    for result in results:
        try:
            item = {
                'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).text,
                'text': result.find(css_identifier_text, first=True).text
            }
            output.append(item)
        except:
            None

    css_identifier_title = "h2"
    css_identifier_link = "a"
    css_identifier_text = "p"

    for result in results:
        try:
            item = {
                'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).attrs['href'],
                'text': result.find(css_identifier_text, first=True).text
            }
            output.append(item)
        except:
            None

    css_identifier_result = ".df_alsoAskCard"

    css_identifier_title = ".df_qntext"
    css_identifier_link = ".b_attribution cite"
    css_identifier_text = ".df_alsocon"

    results = response.html.find(css_identifier_result)

    for result in results:
        try:
            item = {
                'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).text,
                'text': result.find(css_identifier_text, first=True).text
            }
            output.append(item)
        except:
            None

    return output


def bing_search(query):
    response = get_results_bing(query)
    return parse_results_bing(response)


# Data pre-process for TF-IDF NMF

from deep_translator import GoogleTranslator
import spacy

translator = GoogleTranslator(source='auto', target='en')


def translate(text):
    if len(text) < 5000:
        translated = translator.translate(text)
    elif len(text) < 9999:
        translated = translator.translate(text[:4999]) + " " + translator.translate(text[4999:])
    else:
        translated = translator.translate(text[:4999]) + " " + translator.translate(text[4999:9998])

    return translated


def clean_string(ugly_string):
    ugly_string = ugly_string.replace(' ', ' ')
    cleaned_string = [s for s in ugly_string if s.isalpha() or s.isspace()]
    # rejoin intermediate list into a string
    return "".join(cleaned_string)


def isEnglish(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


nlp = spacy.load("en_core_web_md", disable=['parser', 'ner'])


def remove_months_from_text(text, months):
    text2words = text.split()
    result_words = [word for word in text2words if word not in months]
    return ' '.join(result_words)


def only_nouns(texts):
    texts = clean_string(texts)
    if not isEnglish(texts):
        print('Translating..')
        print(texts[:50])
        texts = translate(texts)

    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    doc = nlp(texts)
    noun_text = " ".join(
        token.lemma_.lower() for token in doc if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN' or token.pos_ == 'ADJ'))
    noun_text = remove_months_from_text(noun_text, months)
    return noun_text
