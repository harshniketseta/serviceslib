'''
Created on 27-Jun-2012

@author: harsh
'''
from services import Rest, XMLRPC
from utils import Auth
import pprint

host="preview.ignitelabs.local"
rest_path="restapi"

rest = Rest(host=host, path=rest_path, username="admin", password="admin", auth=Auth.SESSION)
Nodes = rest.retrieve_node(nid=100)
Nodes = Nodes.data
pprint.pprint(Nodes)

xmlrpc_path="xmlrpc"
xmlrpc = XMLRPC(host=host, path=xmlrpc_path)
xmlrpc.login(username="admin", password="admin", auth=Auth.SESSION)

#rest.connect()
#rest.login()