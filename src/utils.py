'''
Created on 25-Jun-2012

@author: harsh
'''

import sys

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
            ty,va,tb = sys.exc_info() #@UnusedVariable
            raise TypeError, "not a valid non-string sequence or mapping object", tb
        
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

