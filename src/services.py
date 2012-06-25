'''
Created on 25-Jun-2012

@author: harsh
'''

import urlparse
import urllib2
from contextlib import closing
from logging import getLogger
from utils import safe_urlencode, ServiceResponse

class BaseService(object):          #docstrings and all added at home.
    '''
    classdocs
    '''
    def __init__(self, fullurl):
        '''
        Constructor
        '''
        
        self.fullurl = fullurl
        
        
    def request(self, method='POST'):
        '''
        
        @param url:
        @param method:
        '''
        def decorator(func):
            def wrapper(*args, **kargs):
                headers, data = func(*args, **kargs)
                useurl = self.fullurl
                headers = headers or {}
                try:
                    data = safe_urlencode(data, doseq=True)
                    if method == 'GET':
                        useurl += '?' + data 
                        data = None
                    
                    parsed = urlparse.urlparse(useurl)      #Making the path URL Quoted
                    useurl = urlparse.urlunparse(parsed[:2]+(urllib2.quote(parsed.path.encode("utf8")),)+parsed[3:])
                    #logging.getLogger().debug("URL = %s", useurl)
                    #logging.getLogger().debug("Headers = %s", headers)
                    #logging.getLogger().debug("Data = %s", data)
                    request = urllib2.Request(url=useurl, data=data, headers=headers)
                    with closing(urllib2.urlopen(request)) as req:
                        retval = ServiceResponse(data=req.read(),headers=req.info())
                        return retval
                except urllib2.HTTPError as err:
                    getLogger().exception('HTTPError: %d', err.code)
                    raise
                except urllib2.URLError as err:
                    getLogger().exception('URLError: %s', err.reason)
                    raise
            return wrapper
        return decorator