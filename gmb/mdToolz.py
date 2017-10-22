#!/usr/bin/python3
# -*- coding: utf-8 -*-

#autor: labruillere @ usual google mail dns
#date: 30/08/2017
#license: bsd

from .fileToolz import fileToArray, create_dir, arrayToFile
from .mdParser import Parser
import base64
from datetime import date
from shutil import copyfile
from random import randrange

class BlogTool :
	''' A simple markdown parser tool '''
	def __init__(self):
		''' init function '''
		self.verbose = 0
		self.blog_title = "mdblog"
		self.allow_tabs = True
		self.css_list = []
		self.js_list = []
		self.page_title = self.blog_title
		self.page_id = ""
		self.default_yield_js = []
		self.default_yield_css = []
		self.aditional_css = []
		self.aditional_js = []
		self.parser = Parser()
		self.aditional_header = []
		self.aditional_footer = []
		self.base_footer = []
		self.base_header = []
		self.file_struct = []
		self.file_struct_len = 0
		self.copy_the_files = False
		self.autor = False
		self.autor_email = False
		self.no_title = False

	def debug(self ,line ,level = 1):
		''' print the debug '''
		if self.verbose >= level or level < 0:
			print ("%s" % line)
	
	def embed_the_html(self, html, header = None):
		'''take some html array and add surounding html'''
		if header == None:
			header = self.base_header
		if self.default_yield_js == [] :
			self.default_yield_js += self.yiel_js_block(self.js_list)
		if self.default_yield_css == [] :
			self.default_yield_css += self.yiel_css_block(self.css_list)
		result_html = ["<!DOCTYPE html>","<html>","<head>","<title>%s</title>" % self.page_title]
		#result_html += ["<meta http-equiv=\"Content-Security-Policy\" content=\"default-src *; style-src 'self' http://* 'unsafe-inline'; script-src 'self' http://* 'unsafe-inline' 'unsafe-eval'\" />"]
		result_html += self.default_yield_css + self.aditional_css
		result_html += ["</head>","<body>","<div id=\"content\">"]
		result_html += header
		result_html += self.aditional_header
		result_html += self.bar()
		result_html += html
		result_html += self.bar()
		result_html += self.parser.yiel_disqus_html(self.page_id)
		result_html += self.aditional_footer
		result_html += self.base_footer
		result_html += ["</div>","<script>"]
		result_html += self.default_yield_js + self.aditional_js
		result_html += ["</script>", "</body>", "</html>" ]
		self.aditional_js = []
		self.aditional_css = []
		return result_html
	
	def yiel_file_struct(self, struct):
		result = []
		for elem in struct:
			if elem[0] == 1 and elem[2][-3:] == ".md":
				result.append(elem)
		return result
	
	def yiel_css_block(self, css_list):
		result = []
		for file_name in css_list:
			#try:
			with open(file_name, "rb") as f:
				encoded_string = base64.b64encode(f.read()).decode()
			result += ['<link rel="stylesheet" href="data:text/css;base64,%s">' % encoded_string]
			#except:
			#	self.debug("unable to add css file '%s'" % file_name,-1)
		return result
		
	def yiel_js_block(self, js_list):
		result = []
		for file_name in js_list:
			try:
				result += fileToArray(file_name)
			except:
				self.debug("unable to add js file '%s'" % filename,-1)
		return result
	
	def copy_files(self,file_list):
		html = []
		for elem in file_list:
			if elem[0] == 0:
				#copy base 64
				pass
			elif elem[0] == 1:
				#copy file
				pass
			else:
				#print bug
				pass
		return html
	
	def parse_markdown(self, working_dir, file_name):
		''' a function that turn markdown array to html, return tuple ( html_array, js_files_to_add, css_files_to_add, (copy_type, files_to_copy_with) )'''
		html = []
		self.parser.verbose = self.verbose
		result = self.parser.parse(working_dir, file_name)
		self.aditional_js = self.yiel_js_block(result[1])
		self.aditional_css = self.yiel_css_block(result[2])
		html += result[0]
		html += self.copy_files(result[3])
		return html
	
	def tabs(self,times=1) :
		self.debug("entering tabed",2)
		#return "<div class=\"tabulation\">&nbsp;</div>"*times
		if self.allow_tabs:
			return "&emsp;"*times
		return ""
	
	def bar(self):
		return ["<div class=\"normal_element\"><div class=\"bar_element\" >&nbsp;</div></div>"]
	
	def build_header(self):
		footer_text = ""
		if self.autor != False:
			if self.autor_email != False:
				footer_text += "<a href=\"mailto:%s?Subject=mail_the_blog\" target=\"_top\">&nbsp;%s&nbsp;%s&nbsp;</a>" % (self.autor_email, self.autor, date.today().year)
			else:
				footer_text += "%s&nbsp;%s" % (self.autor, date.today().year)
		else:
			footer_text += "%s" % (date.today().year)
		self.base_footer =  ["<div class=\"normal_element\"><div class=\"footer\">%s</div></div>" % footer_text]
		if self.no_title == False:
			self.base_header = ["<div class=\"normal_element\"><div class=\"header\" href=\"/\">%s</div></div>" % self.blog_title]
		else:
			self.base_header = [] 
	
	def build_prev_nex_link(self, struct, length, pos):
		'''return a div element containing next and prev links'''
		current_indent = 0 + struct[pos][1]
		home_link = "<a class=\"home_link\" href=\"%sindex.html\">&nbsp;%s&nbsp;</a>" % ("../"*current_indent,self.blog_title)
		rnd_link = self.get_random_link(struct[pos])
		#build prev link
		prev_link = ""
		current_cursor = -1 + pos
		while current_cursor > 0 :
			elem = struct[current_cursor]
			if elem[0] == 1 and elem[2][-3:] == ".md": #regular markdown file
				tmp_link = "/".join(elem[3].split("/")[1:])
				if tmp_link == "":
					tmp_link = "."
				prev_link = "<a class=\"prev_link\" href=\"%s%s/%s.html\">&nbsp;<<&nbsp;</a>" % ("../"*current_indent,tmp_link,elem[2][:-3])
				break
			current_cursor -= 1
		#build next link
		next_link = ""
		current_cursor = 1 + pos
		while current_cursor < length :
			elem = struct[current_cursor]
			if elem[0] == 1 and elem[2][-3:] == ".md": #regular markdown file
				tmp_link = "/".join(elem[3].split("/")[1:])
				if tmp_link == "":
					tmp_link = "."
				next_link = "<a class=\"next_link\" href=\"%s%s/%s.html\">&nbsp;>>&nbsp;</a>" % ("../"*current_indent,tmp_link,elem[2][:-3])
				break
			current_cursor += 1
		
		return ["<div class=\"normal_element\">%s%s%s</div>" % (prev_link,home_link,next_link)], ["<div class=\"normal_element\">%s%s%s</div>" % (prev_link,rnd_link,next_link)]
	
	
	def get_random_link(self,struc_elem):
		maxtime = 10
		while maxtime > -1:
			elem = self.file_struct[randrange(0,self.file_struct_len)]
			if elem != struc_elem:
				break
			maxtime -= 1
		tmp_link = "/".join(elem[3].split("/")[1:])
		if tmp_link == "":
			tmp_link = "."
		return "<a class=\"home_link\" href=\"%s%s/%s.html\">&nbsp;[rnd]&nbsp;</a>" % ("../"*struc_elem[1],tmp_link,elem[2][:-3])
	
	def build(self, tree_struct, target_dir, source_dir):
		''' return a list of html string '''
		indexheader = []
		index = []
		root_dir = "/".join(source_dir.split("/")[:-1])
		self.build_header()
		tree_length = len(tree_struct)
		tree_cursor = 0
		self.file_struct = self.yiel_file_struct(tree_struct)
		self.file_struct_len = 0 + len(self.file_struct)
		while tree_cursor < tree_length:
			elem = tree_struct[tree_cursor]
			if elem[0] == 1: #file
				if elem[1] == 0 and elem[2] == "index.md": #index file found
					indexheader = self.parse_markdown(root_dir + "/" + elem[3] + "/" , elem[2])
					self.debug("index file found")
				elif elem[2][-3:] == ".md" : #regular markdown file
					tmp_link = "/".join(elem[3].split("/")[1:])
					if tmp_link == "":
						tmp_link = "."
					html_link = "%s/%s.html" % (tmp_link, elem[2][:-3])
					#build a nice html links index for the articles, add it to index
					self.page_id = "" + html_link
					index.append("<div class=\"index_element sub-link%s\">%s<a class=\"hyperlink\" href=\"%s\">&nbsp;%s&nbsp;</a></div>"% (elem[1],self.tabs(elem[1]+1),html_link,elem[2][:-3]))
					#build markdown array
					tmp = self.parse_markdown(root_dir + "/" + elem[3] + "/" , elem[2])
					#change page title
					self.page_title = "%s : %s" % (self.blog_title, elem[2][:-3])
					home_link, rnd_link = self.build_prev_nex_link(tree_struct,tree_length,tree_cursor)
					#add aditional header
					self.aditional_header = home_link
					#add additional footer
					self.aditional_footer = rnd_link
					#build page header
					header = ["<div class=\"normal_element\"><div class=\"header\">%s</div></div>" % elem[2][:-3]]
					#add header and footer
					tmp = self.embed_the_html(tmp, header)
					tmp_target_dir = target_dir+"/"+ elem[3] + "/"
					create_dir(tmp_target_dir)
					#turn it into file
					self.debug("creating file '%s'" % tmp_target_dir + elem[2][:-3] + ".html")
					arrayToFile(tmp,tmp_target_dir + elem[2][:-3] + ".html" )
					self.aditional_header = []
					self.aditional_footer = []
				else:
					if self.copy_the_files == True:
						tmp_source_file = "%s/%s/%s" % (root_dir,elem[3], elem[2])
						tmp_target_file = "%s/%s/%s" % (target_dir, elem[3], elem[2])
						self.debug("Copying file from '%s' to '%s'" % (tmp_source_file,tmp_target_file), -1)
						try:
							copyfile(tmp_source_file,tmp_target_file)
						except:
							self.debug("Copy '%s' to '%s'" % (elem[2],tmp_target_file), -1)
					
			elif elem[0] == 0 :
				if elem[1] == 0: # title of the blog
					self.blog_title = "" + elem[2]
					self.debug("title : '%s'" % elem[2])
					self.build_header()
				else: # regular folder
					self.debug("creating folder '%s/%s/'" % (target_dir, elem[3]))
					#build a nice folder like tree html div, add it to index
					index.append("<div class=\"index_element sub-folder%s\"><div class=\"folder\" >%s%s</div></div>" % (elem[1], self.tabs(elem[1]), elem[2]))
					#create the directory
					create_dir("%s/%s/" % (target_dir, elem[3]))
					#print("\t"*elem[1],"  ", elem[2],"[",elem[3],"]")
			else:
				self.debug("cant read tree", -1)
				exit(-1)
			tree_cursor += 1
		#if index header not empty add to index @ start
		if len(indexheader) > 0 :
			self.aditional_header =  indexheader 
		#print(index)
		#index title
		self.page_title = self.blog_title
		#add header and footer to index
		self.page_id = self.blog_title
		index = self.embed_the_html(index)
		#print(index)
		self.debug("%s/%s/index.html" % (target_dir,source_dir.split("/")[-1]))
		#create target dir if don't exist
		create_dir(target_dir)
		#turn into file ( eg: index.html )
		arrayToFile(index,"%s/%s/index.html" % (target_dir,source_dir.split("/")[-1]))
