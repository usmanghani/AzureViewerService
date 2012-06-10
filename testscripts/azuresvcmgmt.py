import requests

r = requests.get("https://management.core.windows.net/993ad3b2-f875-4311-8459-414334cd16ee/services/hostedservices", headers={'x-ms-version':'201-03-01'}, cert='privkey.pem')
print r.status_code
