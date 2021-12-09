# -*- coding: utf-8 -*-
import urllib


def url_encode(query):
    if isinstance(query, bytes):
        query = urllib.quote_plus(query)
    else:
        query = urllib.parse.urlencode(query)
    query = query.replace('+', '%20')
    return query