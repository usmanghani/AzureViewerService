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
	'ROOT_FOLDER' : 'Final_Videos',
	'AUTHOR_EMAIL' : 'productionroadways@gmail.com',
	'VIDEOS_FOLDER' : 'videos_test',
	'VIDEO_TEST_PAGES_FOLDER' : 'videotestpages',
	'IGNORE_CONFLICT_FILES' : True,
	'TEMPLATE_FILENAME' : 'lesson_template.php',
	'TEST_FILE_PREFIX' : 'lesson_',
	'OVERWRITE_EXISTING_TEST_FILES' : False,
	'URL_DUMP_PAGE' : 'urldumps.txt',
	'URL_PREFIX_FOR_DUMPS' : 'http://test.lisanic.com/',
	'URL_DUMP_TEMPLATE_FILE' : 'urldumps_template.html',
}

# if not os.path.exists(CONFIG['VIDEOS_FOLDER']):
# 	os.mkdir(CONFIG['VIDEOS_FOLDER'])

# username = raw_input('Please enter you email address: ')
# password = getpass.getpass()

# docsClient = gdata.docs.service.DocsService()
# docsClient.ClientLogin(username, password)

# document_query = gdata.docs.service.DocumentQuery(categories=['folder'])
# document_query.AddNamedFolder(CONFIG['AUTHOR_EMAIL'], CONFIG['ROOT_FOLDER'])
# feed = docsClient.QueryDocumentListFeed(document_query.ToUri())

# for entry in feed.entry:
# 	title = entry.title.text.encode('UTF-8') 
# 	email = entry.author[0].email.text
# 	feed_url = CONFIG['FEED_URL_PREFIX'] + urllib.quote(entry.resourceId.text) + '/contents?v=3'
# 	document_query = gdata.docs.service.DocumentQuery(feed=feed_url)
# 	inner_feed = docsClient.QueryDocumentListFeed(uri=feed_url)
# 	for inner_entry in inner_feed.entry:
# 		video_title = inner_entry.title.text.encode('UTF-8')
# 		if ('[Conflict]' in video_title) and CONFIG['IGNORE_CONFLICT_FILES']:
# 			continue
# 		media = docsClient.GetMedia(inner_entry.content.src)
# 		print("Downloading file %s(%s) [%s bytes]" % (video_title, media.content_type, media.content_length))
# 		data = media.file_handle.read()
# 		file_path = os.path.join(CONFIG['VIDEOS_FOLDER'], video_title)
# 		if not os.path.exists(file_path):
# 			with open(file_path, 'w') as f:
# 				f.write(data)
# 				f.close()
# 				print("Saved file %s(%s)" % (video_title, media.content_type))
# 		else:
# 			print("File %s(%s) [%s bytes] already exists. Skipping." % (video_title, media.content_type, media.content_length))


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