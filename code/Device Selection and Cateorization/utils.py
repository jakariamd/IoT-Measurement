import json
import ast
import pandas as pd


def decrypt_netdisco(netdisco):
    name = ''
    device_type = ''
    model_name = ''
    manufacturer = ''

    if netdisco.startswith('b\''):
        netdisco_list = eval(netdisco).decode('ISO-8859-1').split('ù¾¸')

        for item in netdisco_list:
            netdisco = json.loads(item)
            try:
                name += netdisco['name']
            except:
                pass
            try:
                name += '+' + netdisco["properties"]["Name"]
            except:
                pass
            try:
                name += '+' + netdisco["properties"]["md"] + '+'
            except:
                pass
            try:
                device_type += netdisco['device_type'] + '+'
            except:
                pass
            try:
                manufacturer += netdisco['manufacturer'] + '+'
            except:
                pass
            try:
                model_name += netdisco['model_name'] + '+'
            except:
                pass

    elif netdisco.startswith('['):
        netdisco_list = eval(netdisco)
        for netdisco in netdisco_list:
            try:
                name += netdisco['name']
            except:
                pass
            try:
                name += '+' + netdisco["properties"]["Name"]
            except:
                pass
            try:
                name += '+' + netdisco["properties"]["md"] + '+'
            except:
                pass
            try:
                device_type += netdisco['device_type'] + '+'
            except:
                pass
            try:
                manufacturer += netdisco['manufacturer'] + '+'
            except:
                pass
            try:
                model_name += netdisco['model_name'] + '+'
            except:
                pass

    return name, device_type, model_name, manufacturer


# decrypt_netdisco(un_inspected_product.loc[332].netdisco_info) un_inspected_product['name'], un_inspected_product[
# 'device_type'], un_inspected_product['model_name'], un_inspected_product['manufacturer'] = zip(
# *un_inspected_product['netdisco_info'].map(decrypt_netdisco))


# function to create a dictionary of mappings
# the functions are created to process the category mapping files


def create_category_dictionary(category_file):
    # category file has 3 columns: 'src_category', 'generic_category', 'src_vendor'
    # iterate all rows of category mapping file
    # output: (src_vendor, src_category) -> generic_category

    category_dictionary = {}

    for index, row in category_file.iterrows():
        src_category = row.src_category
        generic_category = row.generic_category
        src_vendor = ast.literal_eval(row.src_vendor.replace('\n', '').replace("' ", "', "))

        for vendor in src_vendor:
            category_dictionary[(vendor, src_category)] = generic_category

    return category_dictionary


def update_category_dictionary(category_mapping_file, comments_file):
    # update category according to the comment file
    category_dictionary = create_category_dictionary(category_mapping_file)
    comment_dict = create_category_dictionary(comments_file)

    # reflect comments in the main category_dictionary
    for key in comment_dict:
        category_dictionary[key] = comment_dict[key]

    return category_dictionary


def create_df_from_dictionary(category_mapping_file, category_comment_file):
    vendor_category_mapped = update_category_dictionary(category_mapping_file, category_comment_file)
    # read mapping_dict and write it to a list of dict
    dict = []
    for key in vendor_category_mapped:
        dict.append({'src_vendor': key[0], 'src_category': key[1], 'generic_category': vendor_category_mapped[key]})

    return pd.DataFrame.from_dict(dict)

# Finding Super Vendor and subsidiary companies

import requests
import urllib
import json
import pandas as pd
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

http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxies = {
    "http"  : http_proxy,
    "https" : https_proxy,
    "ftp"   : ftp_proxy
}


def get_source(url):
    """Return the source code for the provided URL.
    Args:
        url (string): URL of the page to scrape.
    Returns:
        response (object): HTTP response object from requests_html.
    """
    try:
        #sleep(randint(1,2))
        headers = {'User-Agent': random.choice(user_agent_list)}
        session = HTMLSession()
        response = session.get(url, headers=headers, cookies=g_cookies)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def get_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)   ##response = get_source("https://www.google.co.uk/search?q=" + query)
    return response


def parse_results(response):

    css_identifier_result = ".PZPZlf"
    css_identifier_text = ".FozYP"

    results = response.html.find(css_identifier_result)

    output = []
    for result in results:

        try:
            item = result.find(css_identifier_text, first=True).text
            output.append(item)
        except:
            None

    return output


def google_search(query):
    response = get_results(query)
    return parse_results(response)