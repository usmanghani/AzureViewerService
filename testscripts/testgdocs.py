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
	'ROOT_FOLDER' : 'Lisanic Videos',
	'AUTHOR_EMAIL' : 'productionroadways@gmail.com',
	'VIDEOS_FOLDER' : 'videos_test',
	'VIDEO_TEST_PAGES_FOLDER' : 'videotestpages',
	'IGNORE_CONFLICT_FILES' : True,
	'TEMPLATE_FILENAME' : 'lesson_template.php',
	'TEST_FILE_PREFIX' : 'lesson_',
	'OVERWRITE_EXISTING_TEST_FILES' : False,
	'URL_DUMP_PAGE' : 'urldumps_v2.txt',
	'URL_PREFIX_FOR_DUMPS' : 'http://test.lisanic.com/',
	'URL_DUMP_TEMPLATE_FILE' : 'urldumps_template.html',
	'DOWNLOAD_FLV_ONLY' : True,
	'INCLUDE_EXTENSIONS': ['FLV', 'MP4', 'OGV', 'WEBM'],
	'INCLUDE_DIRS': ['0-99', '100-199', '200-299'],
}

if not os.path.exists(CONFIG['VIDEOS_FOLDER']):
	os.mkdir(CONFIG['VIDEOS_FOLDER'])

username = raw_input('Please enter you email address: ')
password = getpass.getpass()

docsClient = gdata.docs.service.DocsService()
docsClient.ClientLogin(username, password)

root_feed_url = CONFIG['FEED_URL_PREFIX'] + '-/folder' + '?v=3'
# document_query = gdata.docs.service.DocumentQuery(categories=['folder'])
document_query = gdata.docs.service.DocumentQuery(feed=root_feed_url)
# document_query.AddNamedFolder(CONFIG['AUTHOR_EMAIL'], CONFIG['ROOT_FOLDER'])
# feed = docsClient.QueryDocumentListFeed(document_query.ToUri())
root_feed = docsClient.QueryDocumentListFeed(uri=root_feed_url)

for root_entry in sorted(root_feed.entry):
	title = root_entry.title.text.encode('UTF-8') 
	email = root_entry.author[0].email.text
	if title != CONFIG['ROOT_FOLDER']:
		continue
	feed_url = CONFIG['FEED_URL_PREFIX'] + urllib.quote(root_entry.resourceId.text) + '/contents?v=3'
	document_query = gdata.docs.service.DocumentQuery(feed=feed_url)
	feed = docsClient.QueryDocumentListFeed(uri=feed_url)
	for entry in sorted(feed.entry):
		title = entry.title.text.encode('UTF-8') 
		email = entry.author[0].email.text
		print("Looking at folder %s [%s]" % (title, entry.resourceId.text))
		if not title.strip().upper() in CONFIG['INCLUDE_DIRS']:
			print("Skipping folder %s because its not in the list in config." % title)
			continue
		feed_url = CONFIG['FEED_URL_PREFIX'] + urllib.quote(entry.resourceId.text) + '/contents?v=3&max-results=1000'
		document_query = gdata.docs.service.DocumentQuery(feed=feed_url)
		inner_feed = docsClient.QueryDocumentListFeed(uri=feed_url)
		for inner_entry in sorted(inner_feed.entry):
			video_title = inner_entry.title.text.encode('UTF-8')
			if ('[Conflict]' in video_title) and CONFIG['IGNORE_CONFLICT_FILES']:
				continue
			fileNameWithoutExtension, fileExtension = os.path.splitext(video_title)
			if not fileExtension.strip().upper() in CONFIG['INCLUDE_EXTENSIONS']:
			#if not video_title.endswith('.flv') and CONFIG['DOWNLOAD_FLV_ONLY']:
				continue
			print("Checking file %s" % video_title)
			file_path = os.path.join(CONFIG['VIDEOS_FOLDER'], video_title)
			if os.path.exists(file_path):
				print("File %s already exists. Skipping." % video_title)
				continue
			media = docsClient.GetMedia(inner_entry.content.src)
			print("Downloading file %s(%s) [%s bytes]" % (video_title, media.content_type, media.content_length))
			data = media.file_handle.read()
			with open(file_path, 'w') as f:
				f.write(data)
				f.close()
				print("Saved file %s(%s) [%s bytes]" % (video_title, media.content_type, media.content_length))

if not os.path.exists(CONFIG['VIDEO_TEST_PAGES_FOLDER']):
	os.mkdir(CONFIG['VIDEO_TEST_PAGES_FOLDER'])

template_file_contents = str('')

template_file_path = os.path.join(CONFIG['VIDEO_TEST_PAGES_FOLDER'], CONFIG['TEMPLATE_FILENAME'])

with open(template_file_path, 'r') as template_file:
	template_file_contents = template_file.read()
	template_file.close()

with open(CONFIG['URL_DUMP_PAGE'], 'w') as dump_file:
	for video_file in sorted(os.listdir(CONFIG['VIDEOS_FOLDER'])):
		if not video_file.endswith('.flv'):
			continue
		print("Generating test file for %s" % video_file)
		test_filename = os.path.join(CONFIG['VIDEO_TEST_PAGES_FOLDER'], CONFIG['TEST_FILE_PREFIX'] + video_file + '.php')
		dump_file.write(CONFIG['URL_PREFIX_FOR_DUMPS'] + test_filename + '\n\r')
		if os.path.exists(test_filename) and not CONFIG['OVERWRITE_EXISTING_TEST_FILES']:
			print("Test file %s already exists. Skipping." % test_filename)
			continue
		video_file_path = os.path.join('..', CONFIG['VIDEOS_FOLDER'], video_file)
		test_file_content = template_file_contents.replace('[[video_file]]', video_file_path)
		with open(test_filename, 'w') as test_file_to_write:
			test_file_to_write.write(test_file_content)
			print("Wrote file %s for %s" % (test_filename, video_file))
	dump_file.close()
	print("Wrote url dump to %s" % CONFIG['URL_DUMP_PAGE'])
