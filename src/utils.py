'''
Created on 25-Jun-2012

@author: harsh
'''

import sys
import urlparse
import urllib2
from contextlib import closing
from urllib import quote
from functools import wraps
import json

try:
    unicode
except NameError:
    def _is_unicode(x):
        return False
else:
    def _is_unicode(x):
        return isinstance(x, unicode)
    
class Path:
    CONNECT = "system/connect"
    LOGIN = "user/login"
    
class Auth:
    SESSION = "session"
    OAUTH = "oauth"

def dejsonify_response(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        response = func(*args, **kargs)
        response.data = json.loads(response.data)
        return response
    return wrapper

def request(method='POST'):
    '''
    
    @param url:
    @param method:
    '''
    def decorator(func):
        def wrapper(*args, **kargs):
            useurl, headers, data = func(*args, **kargs)
            headers = headers or {}
            try:
                data = safe_urlencode(data, doseq=True)
                if method == 'GET':
                    useurl += '?' + data 
                    data = None
                
                parsed = urlparse.urlparse(useurl)      #Making the path URL Quoted
                useurl = urlparse.urlunparse(parsed[:2]+(urllib2.quote(parsed.path.encode("utf8")),)+parsed[3:])
                print "URL =", useurl
                print "Headers =", headers
                print "Data =", data
                request = urllib2.Request(url=useurl, data=data, headers=headers)
                with closing(urllib2.urlopen(request)) as req:
                    retval = ServiceResponse(data=req.read(),headers=req.info())
                    return retval
            except urllib2.HTTPError as err:
                print('HTTPError: %d', err.code)
                raise
            except urllib2.URLError as err:
                print('URLError: %s', err.reason)
                raise
        return wrapper
    return decorator

def safe_urlencode(query, doseq=0):
    """Encode a sequence of two-element tuples or dictionary into a URL query string.

    If any values in the query arg are sequences and doseq is true, each
    sequence element is converted to a separate parameter.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.
    """

    if hasattr(query,"items"):
        # mapping objects
        query = query.items()
    else:
        # it's a bother at times that strings and string-like objects are
        # sequences...
        try:
            # non-sequence items should not work with len()
            # non-empty strings will fail this
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
            # zero-length sequences of all types will get here and succeed,
            # but that's a minor nit - since the original implementation
            # allowed empty dicts that type of behavior probably should be
            # preserved for consistency
        except TypeError:
            ty,va,tb = sys.exc_info()
            raise TypeError, "not a valid non-string sequence or mapping object", tb

    l = []
    if not doseq:
        # preserve old behavior
        for k, v in query:
            k = quote(str(k))
            v = quote(str(v))
            l.append(k + '=' + v)
    else:
        for k, v in query:
            k = quote(str(k))
            if isinstance(v, str):
                v = quote(v)
                l.append(k + '=' + v)
            elif _is_unicode(v):
                # is there a reasonable way to convert to ASCII?
                # encode generates a string, but "replace" or "ignore"
                # lose information and "strict" can raise UnicodeError
                v = quote(v.encode("ASCII","replace"))
                l.append(k + '=' + v)
            else:
                try:
                    # is this a sufficient test for sequence-ness?
                    len(v)
                except TypeError:
                    # not a sequence
                    v = quote(str(v))
                    l.append(k + '=' + v)
                else:
                    # loop over the sequence
                    for elt in v:
                        l.append(k + '=' + quote(str(elt)))
    return '&'.join(l)
        
class Header(dict):
    ''' Header is a helper class to allow easy additions of headers. Primarily, this formats multi-value headers 
        according to the HTTP specifications (i.e. ';' separated) which is a format suitable for passing to urllib calls
        
        Header supports all standard dict operations
    '''
        
    def __init__(self, *args, **kargs):
        self.update(*args, **kargs)

    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            pass
        else:
            value = self[key] + ';' + value
        finally:
            super(Header, self).__setitem__(key, value)

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("update expected at most 1 arguments, got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]

class ServiceResponse(object):
    '''
    All Responses are packed using this Object.
    '''
    def __init__(self,data, headers):
        '''
        @param data: The data given by response.read()
        @type data: dict
        
        @param headers: The response info given by response.info()
        @type headers: str 
        '''
        self.data = data
        self.headers = headers
    
    def __repr__(self, *args, **kwargs):
        return "Data:{}, Headers:{}".format(self.data, self.headers)
    
if __name__ == '__main__':
    pass

