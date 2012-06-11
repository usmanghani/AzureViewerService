import requests
import httplib

httpsConnection = httplib.HTTPSConnection(host='management.core.windows.net', port=443, cert_file='testcert.pem', key_file='testkey.pem')
httpsConnection.request('GET', '/993ad3b2-f875-4311-8459-414334cd16ee/services/hostedservices', headers={'x-ms-version':'2011-10-01'})
response = httpsConnection.getresponse()
print response.status


#r = requests.get("https://management.core.windows.net/993ad3b2-f875-4311-8459-414334cd16ee/services/hostedservices", headers={'x-ms-version':'201-03-01'}, cert='azuremgmtcert.pfx')
#print r.status_code


