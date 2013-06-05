#!/usr/bin/env python
"""
search.py - Phenny Web Search Module
Copyright 2008-9, Sean B. Palmer, inamidst.com

Copied and changed to sabayon.py - Phenny Web Search for Sabayon.org Pastebin
2013 by Andre Jaenisch
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import urllib
import json
from bs4 import BeautifulSoup
import web


class Grab(web.urllib.URLopener):
    def __init__(self, *args):
        self.version = 'Mozilla/5.0 (Phenny)'
        web.urllib.URLopener.__init__(self, *args)
        self.addheader('Referer', 'https://github.com/sbp/phenny')

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        return web.urllib.addinfourl(fp, [headers, errcode], "http:" + url)


def pastie(number):
    """Search pastebin.sabayon.org/pastie/12728 and return its JSON."""
    """Added by Andre Jaenisch, June 2013"""
    if isinstance(number, unicode):
        number = number.encode('utf-8')
    uri = 'http://pastebin.sabayon.org/pastie/'
    arg = web.urllib.quote(number)
    handler = web.urllib._urlopener
    web.urllib._urlopener = Grab()

    soup = BeautifulSoup(urllib.urlopen(uri + arg))
    lis = soup.find_all('li', 'latest-pastie-item')
    for li in lis:
        if arg in li.a['href']:
            wanted = li

    author = wanted.b.string
    subject = wanted.i.string
    time = wanted.i.next_sibling.next_sibling.next_sibling.strip()

    web.urllib._urlopener = handler
    return json.dumps({'author': author,
                       'subject': subject,
                       'time': time,
                       'url': uri + arg})

if __name__ == '__main__':
    print __doc__.strip()
