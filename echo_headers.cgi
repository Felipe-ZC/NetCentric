#!/usr/bin/python
import sys
import os
sys.stderr = sys.stdout
print "Content-type: text/plain\n"

print "Felipe Zuniga, fzuni005"
print "Accept: ", os.environ['HTTP_ACCEPT']
print "Accept-language:", os.environ['HTTP_ACCEPT_LANGUAGE']
print "Request-method:", os.environ['REQUEST_METHOD']
print "User-agent:", os.environ['HTTP_USER_AGENT']
      
query_str = os.environ.get('QUERY_STRING')
if len(query_str) == 0: 
        print "Query-string: No query string"
else:
        print "Query-string: ", query_str
                                            
