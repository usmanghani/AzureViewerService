import sys
import os
import os.path
import getopt
import getpass
import gdata.docs.service
import gdata.docs.client
import gdata.client
import gdata.spreadsheet.service
import urllib
import httplib
from pprint import pprint

feed_url_prefix = 'https://docs.google.com/feeds/default/private/full/'
root_folder = 'Badar Files'
author_email = 'productionroadways@gmail.com'
username = raw_input('Please enter you email address: ')
password = getpass.getpass()

docsClient = gdata.docs.service.DocsService()
docsClient.ClientLogin(username, password)

document_query = gdata.docs.service.DocumentQuery(categories=['folder'])
document_query.AddNamedFolder(author_email, root_folder)
feed = docsClient.QueryDocumentListFeed(document_query.ToUri())

for entry in feed.entry:
	pprint(entry.content.src)
	title = entry.title.text.encode('UTF-8') 
	pprint(title)
	email = entry.author[0].email.text
	feed_url = feed_url_prefix + urllib.quote(entry.resourceId.text) + '/contents?v=3'
	pprint(feed_url)
	document_query = gdata.docs.service.DocumentQuery(feed=feed_url)
	inner_feed = docsClient.QueryDocumentListFeed(uri=feed_url)
	for inner_entry in inner_feed.entry:
		pprint(inner_entry.title.text.encode('UTF-8'))
		pprint(inner_entry.content.src)
		pprint(inner_entry.content.type)
		media = docsClient.GetMedia(inner_entry.content.src)
		pprint("Details:")
		pprint(media.content_length)
		pprint(media.content_type)
		pprint(media.file_handle)
		data = media.file_handle.read()
		pprint(len(data))
		sys.exit(1)
		