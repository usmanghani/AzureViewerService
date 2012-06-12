import httplib
import urllib2

# HTTPS Client Auth solution for urllib2, inspired by
# http://bugs.python.org/issue3466
# and improved by David Norton of Three Pillar Software. In this
# implementation, we use properties passed in rather than static module
# fields.
class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    def __init__(self, key, cert):
        urllib2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert
    def https_open(self, req):
        #Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)
    def getConnection(self, host, timeout):
        return httplib.HTTPSConnection(host, timeout=timeout, key_file=self.key, cert_file=self.cert)


cert_handler = HTTPSClientAuthHandler('testkey.pem', 'testcert.pem')
opener = urllib2.build_opener(cert_handler)
urllib2.install_opener(opener)

request = urllib2.Request("https://management.core.windows.net/993ad3b2-f875-4311-8459-414334cd16ee/services/hostedservices", headers={"x-ms-version":"2012-03-01"})
f = urllib2.urlopen(request)
print f.read()
print f.code

# httpsConnection = httplib.HTTPSConnection(host='management.core.windows.net', port=443, cert_file='testcert.pem', key_file='testkey.pem')
# httpsConnection.request('GET', '/993ad3b2-f875-4311-8459-414334cd16ee/services/hostedservices', headers={'x-ms-version':'2011-10-01'})
# response = httpsConnection.getresponse()
# print response.status


#r = requests.get("https://management.core.windows.net/993ad3b2-f875-4311-8459-414334cd16ee/services/hostedservices", headers={'x-ms-version':'201-03-01'}, cert='azuremgmtcert.pfx')
#print r.status_code


