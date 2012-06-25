'''
Created on Jun 24, 2012

@author: harsh
'''

import urlparse
import urllib2
from contextlib import closing
from logging import getLogger
from utils import safe_urlencode, ServiceResponse
from urlparse import urljoin

class BaseService(object):
    '''
    A class which contains common logic between REST and XMLRPC.
    '''
    def __init__(self, fullurl):

        if fullurl:
            self.fullurl = fullurl
    
    def getURL(self):
        return self.fullurl
    
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

class Rest(BaseService):
    '''
    A class which lets you make REST calls to your Drupal Site.
    '''
    def __init__(self, host, path):
        '''
        Constructor
        '''
        if host and path:
            super(Rest,self).__init__(fullurl="http://"+urljoin(host, path))
    
class XMLRPC(BaseService):
    '''
    A class which lets you make XMLRPC calls to your Drupal Site.
    '''
    
    def __init__(self, host, path):
        '''
        Constructor
        '''
        if host and path:
            super(XMLRPC,self).__init__(fullurl="http://"+urljoin(host, path))