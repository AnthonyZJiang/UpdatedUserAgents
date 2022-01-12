import urllib.request
import re
import json
import logging

from helper.exceptions import *

HOST_URL_EDGE = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/edge?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=latest-user-agent-index'
HOST_URL_CHROME = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=latest-user-agent-index'
HOST_URL_FIREFOX = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/firefox?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=latest-user-agent-index'

BROWSER_HOSTS = {'edge': HOST_URL_EDGE, 'chrome': HOST_URL_CHROME, 'firefox': HOST_URL_FIREFOX}
PLATFORM_NAMES = {'windows': 'Win64', 'macos': 'Macintosh', 'android': 'Android', 'ios': 'iPhone'}


def read_local_ua():
    with open('useragents.json', 'r') as f:
        return json.load(f)


def get_empty_UA():
    return {
        'windows': '',
        'macos': '',
        'android': '',
        'ios': ''
    }


def fetch_UA(url):
    with urllib.request.urlopen(url) as response:
        if response.code != 200:
            raise UAFetchError(f'Failed to fetch UA from {url}')
        html = response.read().decode('utf-8')
    logging.info('Response received.')
    return parse_UA(html)


def parse_UA(html):
    regex = r'<span class="code">(.*?)</span>'
    uas = re.findall(regex, html)
    if not uas:
        raise UAParseError('No UA found in the response.')
    ua_result = get_empty_UA()
    for ua in uas:
        for platform in PLATFORM_NAMES.keys():
            if ua_result[platform] != '':
                continue
            if ua.find(PLATFORM_NAMES[platform]) != -1:
                ua_result[platform] = ua
                print(f'{platform: <10} {ua}')
                break
    logging.info(f'Response parsed. {len(ua_result)} UA found.')
    return ua_result


def is_UA_unchanged(remote_UA, local_UA):
    return all(
        remote_UA[platform] == local_UA[platform]
        for platform in PLATFORM_NAMES.keys()
    )


def update_all_from_remote():
    old_UA = read_local_ua()
    new_UA = old_UA
    flag = 0
    for browser in BROWSER_HOSTS.keys():
        logging.info(f'Fetching UA for {browser}...')
        try:
            new_UA[browser] = fetch_UA(BROWSER_HOSTS[browser])
        except (UAFetchError, UAParseError) as e:
            logging.error(e, exc_info=True)
            continue
        if not is_UA_unchanged(new_UA[browser], old_UA[browser]):
            flag = True
    return flag, new_UA
