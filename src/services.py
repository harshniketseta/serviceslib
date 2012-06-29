'''
Created on Jun 24, 2012

@author: harsh
'''
from utils import request, Path, Auth, dejsonify_response, Header
import xmlrpclib
import pprint
from urllib2 import HTTPError

class Invalid_Parameters_Exception(Exception):
    pass


class BaseService(object):
    '''
    A class which contains common logic between REST and XMLRPC.
    '''
    def __init__(self, host, path, username=None, password=None, auth=None, oauth_key=None):
        
        self.fullurl = "http://{host}/{path}".format(host=host, path=path)
        
        if auth == Auth.OAUTH and oauth_key:
            self.do_oauth_login(username=username, password=password)

        elif username and password and auth == Auth.SESSION:
            self.do_session_login(username=username, password=password)
#            print "Auth Header:",self.auth_header
#            print "User:"
#            pprint.pprint(self.user)
        else:
            raise Invalid_Parameters_Exception

    def getURL(self):
        return self.fullurl
    
    def get_user(self):
        return self.user
    
    def add_auth_header(self, headers):
        headers = headers or Header()
        headers["Cookie"] = self.auth_header
        return headers
    
class Rest(BaseService):
    '''
    A class which lets you make REST calls to your Drupal Site.
    '''
    
    def do_session_login(self, username, password):
        connect = self.connect()
        self.sessid = connect.data['sessid']
        
        login = self.login(username=username, password=password, sessid=self.sessid)
        self.auth_header = "{session_name}={sessid}".format(session_name=login.data["session_name"], sessid=login.data['sessid'])
        self.user = login.data['user']
    
    def do_oauth_login(self, username, password):
        pass
        
    @dejsonify_response
    @request(method='POST')
    def connect(self, headers=None, **kargs):
        return "{host}/{path}".format(host=self.fullurl, path=Path.CONNECT), headers, ""
    
    @dejsonify_response
    @request(method='POST')
    def login(self, headers=None, **kargs):
        return "{host}/{path}".format(host=self.fullurl, path=Path.LOGIN), headers, kargs
    
    @dejsonify_response
    @request(method='GET')
    def retrieve_node(self, nid='', headers=None, **kargs):
        try:
            return "{host}/{path}/{nid}".format(host=self.fullurl, path=Path.NODERETRIEVE, nid=nid), self.add_auth_header(headers), kargs
        except HTTPError:
            print "HTTPERROR Occur"
            return None
    
    @dejsonify_response
    @request(method='GET')
    def retrieve_user(self, headers=None, **kargs):
        return "{host}/{path}".format(host=self.fullurl, path=Path.USERRETRIEVE), self.add_auth_header(headers), kargs
    
class XMLRPC(BaseService):
    '''
    A class which lets you make XMLRPC calls to your Drupal Site.
    '''
    
    def do_session_login(self, username, password):
        connect = self.connect()
        self.sessid = connect['sessid']
        
        login = self.login(username=username, password=password, sessid=self.sessid)
        self.auth_header = "{session_name}={sessid}".format(session_name=login["session_name"], sessid=login['sessid'])
        self.user = login['user']
    
    def do_oauth_login(self, username, password):
        pass
                    
    def connect(self, **kargs):
        self.xmlrpc_server = xmlrpclib.Server(self.fullurl)
        return self.xmlrpc_server.system.connect()
    
    def login(self, **kargs):
        return self.xmlrpc_server.user.login(*kargs.values())
        