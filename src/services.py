'''
Created on Jun 24, 2012

@author: harsh
'''
from duplicity.urlparse_2_5 import urljoin

class BaseService(object):
    '''
    A class which contains common logic between REST and XMLRPC.
    '''
    def __init__(self, fullurl):
        '''
        Constructor
        '''
        if fullurl:
            self.fullurl = fullurl
    
    def getURL(self):
        return self.fullurl
    
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