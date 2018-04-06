from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import warnings
import inspect

from .compat import urlparse


def check_uri_security(uri):
    """ Warns if the uri is insecure. """
    if urlparse(uri).scheme != 'https':
        warning_message = (
            """\n\nWARNING: this client is sending a request to an insecure API endpoint. Any API request you make may expose your API key and secret to third parties. Consider using the default or a secure endpoint: \n\n\'%s\'\n
            """) % uri.replace('http','https')
        warnings.warn(warning_message, UserWarning)
    return uri


def method_name():
    """
    Returns the current active function name as a string
    """
    return inspect.stack()[1][3]
