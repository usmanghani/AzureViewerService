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
	'FEED_URL_SUFFIX' : '?v=3&max-results=1000',
	'ROOT_FOLDERS' : ['Lisanic Videos'],
	'AUTHOR_EMAIL' : 'productionroadways@gmail.com',
	'VIDEOS_FOLDER' : 'videos_test',
	'VIDEO_TEST_PAGES_FOLDER' : 'videotestpages',
	'IGNORE_CONFLICT_FILES' : True,
	'TEMPLATE_FILENAME' : 'lesson_template.php',
	'TEST_FILE_PREFIX' : 'lesson_',
	'OVERWRITE_EXISTING_VIDEO_FILES' : True,
	'OVERWRITE_EXISTING_TEST_FILES' : False,
	'URL_DUMP_PAGE' : 'urldumps_v2.txt',
	'URL_PREFIX_FOR_DUMPS' : 'http://test.lisanic.com/',
	'URL_DUMP_TEMPLATE_FILE' : 'urldumps_template.html',
	'DOWNLOAD_FLV_ONLY' : True,
	'INCLUDE_EXTENSIONS': ['.FLV', '.MP4', '.OGV', '.WEBM'],
	'INCLUDE_DIRS': ['0-199', '200-299', '300-399'],
	'CORRECTION_DIRS': ['0-199 CORRECTIONS', '200-299 CORRECTIONS', '300-399 CORRECTIONS'],
}

def init_videos_folder():
	if not os.path.exists(CONFIG['VIDEOS_FOLDER']):
		os.mkdir(CONFIG['VIDEOS_FOLDER'])

def get_creds():
	username = raw_input('Please enter you email address: ')
	password = getpass.getpass()
	return (username, password)

def get_root_folder_feed():
	return __get_folder_feed('-/folder')

def get_folder_feed(folder_name):
	return __get_folder_feed(urllib.quote(folder_name) + '/contents')

def __get_folder_feed(url_partial):
	feed_url = CONFIG['FEED_URL_PREFIX'] + url_partial + CONFIG['FEED_URL_SUFFIX']
	feed = docsClient.QueryDocumentListFeed(uri=feed_url)
	return feed

def get_title_and_email(feed_entry):
	title = feed_entry.title.text.encode('UTF-8') 
	email = feed_entry.author[0].email.text
	return (title, email)

def download_video_files(file_feed, remove_spaces_from_filenames = True, force_overwrite = False):
	for file_entry in sorted(file_feed.entry):
		video_title, email = get_title_and_email(file_entry)
		print("Checking file %s" % video_title)
		if ('[Conflict]' in video_title) and CONFIG['IGNORE_CONFLICT_FILES']:
			print("Skipping file %s because it is a conflict file." % video_title)
			continue
		fileNameWithoutExtension, fileExtension = os.path.splitext(video_title)
		if not fileExtension.strip().upper() in CONFIG['INCLUDE_EXTENSIONS']:
			print("Skipping file %s with extension %s because it doesn't have an extension included in the list." % (video_title, fileExtension.strip().upper()))
			continue
		
		file_path = os.path.join(CONFIG['VIDEOS_FOLDER'], video_title)
		if (remove_spaces_from_filenames):
			file_path = os.path.join(CONFIG['VIDEOS_FOLDER'], video_title.strip().replace(' ', ''))

		if not force_overwrite and os.path.exists(file_path) and not CONFIG['OVERWRITE_EXISTING_VIDEO_FILES']:
			print("File %s already exists. Skipping." % video_title)
			continue
		media = docsClient.GetMedia(file_entry.content.src)
		print("Downloading file %s(%s) [%s bytes]" % (video_title, media.content_type, media.content_length))
		data = media.file_handle.read()
		with open(file_path, 'w') as f:
			f.write(data)
			f.close()
			print("Saved file %s(%s) [%s bytes]" % (video_title, media.content_type, media.content_length))

def write_test_files():
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

if __name__ == '__main__':
	init_videos_folder()
	username, password = get_creds()

	docsClient = gdata.docs.service.DocsService()
	docsClient.ClientLogin(username, password)

	root_feed = get_root_folder_feed()

	for root_entry in sorted(root_feed.entry):
		title, email = get_title_and_email(root_entry)
		print("Looking at folder %s [%s]" % (title, root_entry.resourceId.text))
		if title.strip().upper() in CONFIG['ROOT_FOLDERS']:
			continue

		feed = get_folder_feed(root_entry.resourceId.text)
		
		correction_dir_list = []
		
		for entry in sorted(feed.entry):
			title, email = get_title_and_email(entry)
			print("Looking at folder %s [%s]" % (title, entry.resourceId.text))
			if not title.strip().upper() in CONFIG['INCLUDE_DIRS']:
				if title.strip().upper() in CONFIG['CORRECTION_DIRS']:
					print("Skipping folder %s because its a correction folder." % title)
					correction_dir_list.append(entry)
				else:
					print("Skipping folder %s because its not in the list in config." % title)
				continue
			file_feed = get_folder_feed(entry.resourceId.text)
			download_video_files(file_feed)

		# handle corrections
		for correction_dir_entry in correction_dir_list:
			title, email = get_title_and_email(correction_dir_entry)
			print("Looking at corrections folder %s [%s]" % (title, entry.resourceId.text))
			file_feed = get_folder_feed(entry.resourceId.text)
			download_video_files(file_feed, force_overwrite = True)
			

	write_test_files()
