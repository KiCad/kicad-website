# pip install gitpython

import sys, os, fileinput
import shutil
from git import Repo

KICADDOC_PATH = "kicad-doc"
REMOTE_URL = "https://github.com/ciampix/kicad-doc.git"

CONTENT_PATH = "content"
DOCS_PATH = "docs"
DEST_PATH = CONTENT_PATH+"/"+DOCS_PATH

def main():
	pull_repo()
	copy_adocs()
	update_adoc_paths()

def pull_repo():
	if os.path.isdir(KICADDOC_PATH):
		print "KiCad Docs folder exists, attempting git pull to update"
		repo = Repo(KICADDOC_PATH)
		o = repo.remotes.origin
		o.pull()
	else:
		print "KiCad Docs folder does not exist, attempting to clone"
		Repo.clone_from(REMOTE_URL, KICADDOC_PATH)
		assert cloned_repo.__class__ is Repo

#
#	Copy over adocs from the git folder to the hugo content folder
#	Right now it just tries to copy .adoc and .png files
#   Also my python is bad and the path maniupulation for output looks silly
#
def copy_adocs():
	print "Copying over fresh doc files to hugo"
	search_path = KICADDOC_PATH+"/src/"

	for root, dirs, files in os.walk(search_path):
		for file in files:
			if file.endswith(".adoc") or file.endswith(".png"):
				src_path = os.path.join(root, file)
				dest_path = os.path.join(DEST_PATH, src_path.replace(search_path,''))
				shutil.copyfile(src_path, dest_path)
				

# 
#	Process adoc files in the hugo content folder to have correct paths
#	Hugo/asciidoctor use the root of the hugo site to generate includes
#	And if we don't update the paths from kicad-doc, the includes won't work
#
def update_adoc_paths():
	print "Rewriting adoc include paths"
	for root, dirs, files in os.walk(DEST_PATH):
		for file in files:
			if file.endswith(".adoc"):
				update_adoc_path(root, file)
				
				
def update_adoc_path(root, file):
	filePath = os.path.join(root, file)
	replaceIncludeText = "include::" + root + "\\"
	print replaceIncludeText
	replaceImageText = "image:" + root.replace(CONTENT_PATH,'') + "\\"
	print replaceImageText

	for line in fileinput.input(filePath, inplace=True):
		line = line.replace('include::', replaceIncludeText)
		line = line.replace('image:', replaceImageText)
		print(line)
	

if __name__ == '__main__':
    main()