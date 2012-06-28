'''
Created on Jun 24, 2012

@author: harsh
'''
from utils import request, Path, Auth, dejsonify_response
from urlparse import urljoin
import pprint


class Invalid_Parameters_Exception(Exception):
    pass


class BaseService(object):
    '''
    A class which contains common logic between REST and XMLRPC.
    '''
    def __init__(self, fullurl, username=None, password=None, auth=None, oauth_key=None):

        self.fullurl = fullurl
        print self.fullurl
        if auth == Auth.OAUTH and oauth_key == None:
            raise Invalid_Parameters_Exception   

        if username and password:
            connect = self.connect()
            self.sessid = connect.data['sessid']
            
            login = self.login(username=username, password=password, sessid=self.sessid)
            self.auth_header = "{session_name}={sessid}".format(session_name=login.data["session_name"], sessid=login.data['sessid'])
            self.user = login.data['user']
            
#            print "Auth Header:",self.auth_header
#            print "User:"
#            pprint.pprint(self.user)
    
    def getURL(self):
        return self.fullurl
    
    @dejsonify_response
    @request(method='POST')
    def connect(self, **kargs):
        return "{host}/{path}".format(host=self.fullurl, path=Path.CONNECT), None, ""
    
    @dejsonify_response
    @request(method='POST')
    def login(self, **kargs):
        return "{host}/{path}".format(host=self.fullurl, path=Path.LOGIN), None, kargs
    
    def get_user(self):
        return self.user

class Rest(BaseService):
    '''
    A class which lets you make REST calls to your Drupal Site.
    '''
    def __init__(self, host, path, *args, **kargs):
        '''
        Constructor
        '''
        if host and path:
            super(Rest,self).__init__(fullurl="http://{host}/{path}".format(host=host, path=path) , *args, **kargs)
    
class XMLRPC(BaseService):
    '''
    A class which lets you make XMLRPC calls to your Drupal Site.
    '''
    
    def __init__(self, host, path, *args, **kargs):
        '''
        Constructor
        '''
        if host and path:
            super(XMLRPC,self).__init__(fullurl="http://{host}/{path}".format(host=host, path=path), *args, **kargs)