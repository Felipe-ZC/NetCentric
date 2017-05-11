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
print "Query-string:" ,os.environ['QUERY_STRING']

