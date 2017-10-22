#!/usr/bin/python3
# -*- coding: utf-8 -*-

#autor: labruillere @ usual google mail dns
#date: 30/08/2017
#license: bsd

from gmb.mdToolz import BlogTool
from gmb.fileToolz import Tree
from os.path import abspath, isdir
from optparse import OptionParser

self_verbose = 0
def debug(line ,level = 1):
	''' print the debug '''
	if self_verbose >= level or level < 0:
		print ("%s" % line)

if __name__ == "__main__" :
	usage = "Usage: %prog -i [md folder] -o [dest folder] {options}"
	opt_parser = OptionParser(usage=usage)
	opt_parser.add_option("-i", "--input-folder", dest="input",
                  help="Path to the folder containing the markdowns", default=False)
	opt_parser.add_option("-o", "--output-folder", dest="output",
                  help="Path to the output folder", default=False)
	opt_parser.add_option("-v", "--verbose", dest="verbose",
                  help="Verbosity level", default=0, type="int")
	opt_parser.add_option("-q", "--quiet",
                  action="store_true", dest="quiet", default=False,
                  help="don't print status messages to stdout")
	opt_parser.add_option("-t", "--allow-tabs",
                  action="store_true", dest="tabs", default=False,
                  help="Add tabulations to index page entries")
	opt_parser.add_option("-l", "--layout", dest="layout", default=False,
                  help="use different css layout")
	opt_parser.add_option("-a", "--aditional-layout", dest="aditional", default=False,
                  help="Use an aditional layout")
	opt_parser.add_option("-d", "--discus-user", dest="discus", default=False,
                  help="Add discus comments to pages")
	opt_parser.add_option("-c", "--copy-files",
                  action="store_true", dest="copy", default=False,
                  help="Copy files contained in folders")
	opt_parser.add_option("-b", "--blogger-name", dest="blogger",
                  help="the blogger name", default=False)
	opt_parser.add_option("-e", "--blogger-email", dest="email",
                  help="Blogger email", default=False)
	opt_parser.add_option("-p", "--poster", dest="notitle",action="store_true",
                  help="Remove title from index", default=False)
    
	( options, args ) = opt_parser.parse_args()
	self_verbose = options.verbose
	#from sys import argv
	#program_name, markdown_folder, target_forler = argv
	if options.input == False:
		opt_parser.print_help()
		exit(-1)
	if options.output == False:
		opt_parser.print_help()
		exit(-1)
	markdown_folder = options.input
	if isdir(markdown_folder):
		markdown_folder = abspath(markdown_folder)
		
		debug( "dir is: %s" % markdown_folder)
		tree_representation = Tree(markdown_folder)
		debug( "parsing ...")
		if self_verbose > 0:
			tree_representation.print_list()
		blog_tool = BlogTool()
		blog_tool.verbose = options.verbose
		if options.quiet :
			blog_tool.verbose = -1
		blog_tool.allow_tabs = options.tabs
		blog_tool.autor = options.blogger
		blog_tool.autor_email = options.email
		blog_tool.copy_the_files = options.copy
		blog_tool.no_title = options.notitle
		blog_tool.css_list = ["gmb/prism.css"]
		if options.layout :
			blog_tool.css_list += ["" + str(options.layout)]
		else:
			blog_tool.css_list += ["gmb/default_layout.css"]
		if options.aditional:
			blog_tool.css_list += ["" + str(options.aditional)]
		blog_tool.js_list = ["gmb/prism.js"]
		blog_tool.parser.disqus_id = options.discus
		blog_tool.build(tree_representation.list, options.output, markdown_folder)
	else:
		print( "please use a directory as parameter")
