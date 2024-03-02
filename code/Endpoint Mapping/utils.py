import tldextract
import ast
from cleanco import basename
import unicodedata
import re
from publicsuffixlist import PublicSuffixList

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import string

import abydos.distance as abd
from thefuzz import fuzz


def clean_flow(flow_df):
    flow_df = flow_df[~(flow_df['remote_hostname'] == '(Local Network)')]
    flow_df = flow_df[flow_df['remote_port'] != 53]
    flow_df = flow_df[flow_df['remote_port'] != 123]
    flow_df = flow_df[flow_df['remote_hostname'].notnull()]
    flow_df = flow_df[~(flow_df['remote_hostname'].str.startswith('192.168'))]
    flow_df = flow_df[~(flow_df['remote_hostname'] == '')]
    return flow_df


def get_sld(query):
    try:
        ext = tldextract.extract(query)
        if ext.domain and ext.suffix:
            ext = ext.domain + '.' + ext.suffix
        else:
            ext = None
    except:
        ext = None
    return ext


# This function is defined to combined data from different sources and find the unique results
# Input: organization name from different domain
# Output: Unique organization names

# update suffix list periodically
suffix_list = ['365', ' and', 'board', 'branch', 'business', 'cable', 'canada', 'center',
               'china', 'communications', 'company', 'corporation', 'data', 'digital', 'electronics', 'european',
               ' for', 'foundation', 'global', 'groups', 'group', 'holdings', 'holding', 'india', 'information',
               'international',
               'internet', 'media', 'mobile', 'networks', 'network', 'news', ' of', 'office', 'policy', 'privacy',
               'products', 'public', 'services', 'service', 'software', 'solutions', 'solution', 'sports', 'store',
               'support',
               'systems', 'system', 'technologies', 'technology', 'telecom', 'telephone', 'television', 'the ', 'tv',
               'union', '2022', '2021', '2023']


def get_only_sld(query):
    try:
        ext = tldextract.extract(query)
        if ext.domain:
            ext = ext.domain
        else:
            ext = None
    except:
        ext = None

    return ext


def unique_domain2org(domain, python_whois_org, bash_whois_org, bash_openssl_org, copyright_org, netify_org,
                      xclusive_org):
    combined_org = [python_whois_org, bash_whois_org, bash_openssl_org, netify_org, xclusive_org]

    try:
        copyright_org = ast.literal_eval(copyright_org)
        # string to list #webpage_org = ast.literal_eval(webpage_org) #combined_org.extend(webpage_org)
        combined_org.extend(copyright_org)
    except:
        None
    sld = get_only_sld(domain)
    if sld: combined_org.append(sld)
    if sld.startswith('my'): combined_org.append(sld[2:])

    combined_org = [org for org in combined_org if org]

    cleaned_list = []

    for name in combined_org:
        try:
            cleaned_name = name.lower()  # lowering all capital letters.
            for suffix in suffix_list:
                cleaned_name = cleaned_name.replace('' + suffix, '')
            cleaned_name = unicodedata.normalize('NFKD', cleaned_name).encode('ASCII',
                                                                              'ignore').decode()  # replace non-ASCII characters
            cleaned_name = re.sub(r'[^\w\s]', '', cleaned_name)  # remove punctuation
            cleaned_name = basename(cleaned_name)  # base form of the name
            cleaned_name = basename(cleaned_name)  # base form of the name
            cleaned_name = basename(cleaned_name)  # base form of the name
            cleaned_name = basename(cleaned_name)  # base form of the name

            if cleaned_name:
                cleaned_list.append(cleaned_name)
        except:
            None

    return list(set(cleaned_list))


# This function find unique organization names from vendor organization, 
# parent organization and subsidiary organizations 

def unique_org_name(device_vendor, vendor_org, parent_org, subsidiaries):
    subsidiaries = ast.literal_eval(subsidiaries)
    subsidiaries.extend([device_vendor, vendor_org, parent_org])

    cleaned_list = []

    for name in subsidiaries:
        try:
            cleaned_name = name.lower()  # removing all capital letters.
            for suffix in suffix_list:
                cleaned_name = cleaned_name.replace(' ' + suffix, '')
            cleaned_name = unicodedata.normalize('NFKD', cleaned_name).encode('ASCII',
                                                                              'ignore').decode()  # replace non-ASCII characters
            cleaned_name = re.sub(r'[^\w\s]', '', cleaned_name)  # remove punctuation
            cleaned_name = basename(cleaned_name)  # base form of the name
            cleaned_name = basename(cleaned_name)  # base form of the name
            cleaned_name = basename(cleaned_name)  # base form of the name
            cleaned_name = basename(cleaned_name)  # base form of the name

            if cleaned_name:
                cleaned_list.append(cleaned_name)
        except:
            None

    return list(set(cleaned_list))


def get_sld(query):
    try:
        ext = tldextract.extract(query)
        if ext.domain and ext.suffix:
            ext = ext.domain + '.' + ext.suffix
        else:
            ext = None
    except:
        ext = None

    return ext


# uses built-in PSL file
psl = PublicSuffixList()


def get_tld_plus_1(remote_hostname):
    try:
        tld_plus_1 = psl.privatesuffix(remote_hostname)
    except:
        tld_plus_1 = None

    return tld_plus_1


def get_device_connections(data, device_vendor, device_name):
    device_data = data[(data['device_vendor'] == device_vendor) & (data['device_name'] == device_name)]

    # print(device_data)
    # removing dns and ntp query
    device_data = device_data[(device_data['remote_port'] != 53)]
    device_data = device_data[(device_data['remote_port'] != 123) | (device_data['protocol'] != 'udp')]
    device_data.dropna(subset=['remote_hostname'], inplace=True)

    # get top level domain + 1
    device_data['tld_plus_1'] = device_data.apply(lambda row: get_sld(row.remote_hostname), axis=1)
    # device_data['tld_plus_1'] = device_data['tld_plus_1'].str.replace('?','')

    return device_data.tld_plus_1.unique()


def print_statistics(device_data):
    print("No of unique unique devices: ", len(device_data.device_id.unique()))
    print("No of unique unique users: ", len(device_data.user_key.unique()))
    print("Unique remote hosts: ", device_data.tld_plus_1.unique())
    print("Unique ports: ", device_data.remote_port.unique())



# This function decides the first party relationship
# Input: list of vendor organization names and domain organization names
# Output: True if first-party, False if not

def mapping_first_party(vendor_org,  domain_org):
    fuzzy_similarity = 0
    levenshtein_similarity = 0
    ssk_similarity = 0
    max_ = 0


    for v_org in vendor_org:
        for d_org in domain_org:
            if (len(v_org)>100) or (len(d_org)>100):
                return 0
            lvsn_sim = abd.DiscountedLevenshtein().sim(v_org, d_org)
            ssk_sim = abd.SSK().sim(v_org, d_org)
            fuzz_sim = fuzz.token_sort_ratio(v_org, d_org)/100

            if levenshtein_similarity < lvsn_sim:
                levenshtein_similarity = lvsn_sim

            if ssk_similarity < ssk_sim:
                ssk_similarity = ssk_sim

            if fuzzy_similarity < fuzz_sim:
                fuzzy_similarity = fuzz_sim

            if max_ <  max(levenshtein_similarity, ssk_similarity, fuzzy_similarity):
                max_ = max(levenshtein_similarity, ssk_similarity, fuzzy_similarity)
            #print(v_org, '-vs.' , d_org, max_)
            '''
            if fuzz.partial_ratio(v_org, d_org) > fuzzy_score:
                fuzzy_score = fuzz.partial_ratio(v_org, d_org)
                print(v_org, '-vs.' ,  d_org, fuzz.partial_ratio(v_org, d_org), fuzz.ratio(v_org, d_org))
            '''

    if max_ > 0.90:
        return 1
    return 0

