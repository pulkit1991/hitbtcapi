# coding: utf-8
import inspect
import six

if six.PY2:
    from itertools import imap
    from urllib import quote
    from urlparse import urlparse
    # from urlparse import urlencode

elif six.PY3:
    imap = map
    from urllib.parse import quote
    from urllib.parse import urlparse
    # from urllib.parse import urlencode
