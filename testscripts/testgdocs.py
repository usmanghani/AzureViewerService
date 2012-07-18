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

CONFIG = {
	'FEED_URL_PREFIX' : 'https://docs.google.com/feeds/default/private/full/',
	'ROOT_FOLDER' : 'Badar Files',
	'AUTHOR_EMAIL' : 'productionroadways@gmail.com',
	'VIDEOS_FOLDER' : 'videos'
}

if not os.path.exists(CONFIG['VIDEOS_FOLDER']):
	os.mkdir(CONFIG['VIDEOS_FOLDER'])

username = raw_input('Please enter you email address: ')
password = getpass.getpass()

docsClient = gdata.docs.service.DocsService()
docsClient.ClientLogin(username, password)

document_query = gdata.docs.service.DocumentQuery(categories=['folder'])
document_query.AddNamedFolder(CONFIG['AUTHOR_EMAIL'], CONFIG['ROOT_FOLDER'])
feed = docsClient.QueryDocumentListFeed(document_query.ToUri())

for entry in feed.entry:
	title = entry.title.text.encode('UTF-8') 
	email = entry.author[0].email.text
	feed_url = CONFIG['FEED_URL_PREFIX'] + urllib.quote(entry.resourceId.text) + '/contents?v=3'
	document_query = gdata.docs.service.DocumentQuery(feed=feed_url)
	inner_feed = docsClient.QueryDocumentListFeed(uri=feed_url)
	for inner_entry in inner_feed.entry:
		video_title = inner_entry.title.text.encode('UTF-8')
		media = docsClient.GetMedia(inner_entry.content.src)
		print("Downloading file %s(%s) [%s bytes]" % (video_title, media.content_type, media.content_length))
		data = media.file_handle.read()
		file_path = os.path.join(CONFIG['VIDEOS_FOLDER'], video_title)
		if not os.path.exists(file_path):
			with open(file_path, 'w') as f:
				f.write(data)
				f.close()
				print("Saved file %s(%s)" % (video_title, media.content_type))
		else:
			print("File %s(%s) [%s bytes] already exists. Skipping." % (video_title, media.content_type, media.content_length))