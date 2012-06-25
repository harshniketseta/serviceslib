'''
Created on Jun 24, 2012

@author: harsh
'''
import unittest
from services import BaseService, Rest, XMLRPC
from urlparse import urljoin

class inittest(unittest.TestCase):

    def setUp(self):
        
        self.host = "www.harshniketseta.local"
        self.path = "testpath"
        
        self.base = BaseService("http://"+urljoin(self.host, self.path))
        
        self.rest = Rest(self.host, self.path)
        self.xmlrpc = XMLRPC(self.host, self.path)

    def testrestinit(self):
        self.assertEqual(self.base.getURL(), self.rest.getURL())

    
    def testXMLRPCinit(self):
        self.assertEqual(self.base.getURL(), self.xmlrpc.getURL())

def suite():
    '''
    Creating a suite of tests to be run.
    
    @return: A suite of tests to be run.
    @rtype: TestSuite
    '''
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(inittest))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())