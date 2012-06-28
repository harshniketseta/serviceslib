'''
Created on Jun 24, 2012

@author: harsh
'''
from utils import request, Path, Auth, dejsonify_response
import xmlrpclib

class Invalid_Parameters_Exception(Exception):
    pass


class BaseService(object):
    '''
    A class which contains common logic between REST and XMLRPC.
    '''
    def __init__(self, **kargs):
        self.initialize()

    def getURL(self):
        return self.fullurl
    
    def initialize(self, fullurl, username=None, password=None, auth=None, oauth_key=None):
        self.fullurl = fullurl
        print self.fullurl
        if auth == Auth.OAUTH and oauth_key:
            pass

        elif username and password and auth == Auth.SESSION:
            connect = self.connect()
            self.sessid = connect.data['sessid']
            
            login = self.login(username=username, password=password, sessid=self.sessid)
            self.auth_header = "{session_name}={sessid}".format(session_name=login.data["session_name"], sessid=login.data['sessid'])
            self.user = login.data['user']
            
#            print "Auth Header:",self.auth_header
#            print "User:"
#            pprint.pprint(self.user)
        else:
            raise Invalid_Parameters_Exception

    
    @dejsonify_response
    @request(method='POST')
    def rest_connect(self, **kargs):
        return "{host}/{path}".format(host=self.fullurl, path=Path.CONNECT), None, ""
    
    @dejsonify_response
    @request(method='POST')
    def rest_login(self, **kargs):
        return "{host}/{path}".format(host=self.fullurl, path=Path.LOGIN), None, kargs

    def xmlrpc_initialize(self):
        pass
        
    def xmlrpc_connect(self, **kargs):
        self.xmlrpc_server = xmlrpclib.Server(self.fullurl)
        return self.xmlrpc_server.system.connect()
    
    def xmprpc_login(self, **kargs):
        self.xmlrpc_server.user.login(**kargs)
    
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
#        self.initialize = self.rest_initialize
        self.connect = self.rest_connect
        self.login = self.rest_login
        
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
#        self.initialize = self.xmlrpc_initialize
        self.connect = self.xmlrpc_connect
        self.login = self.xmlrpc_login
        
        if host and path:
            super(XMLRPC,self).__init__(fullurl="http://{host}/{path}".format(host=host, path=path), *args, **kargs)

