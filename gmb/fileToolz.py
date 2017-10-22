#!/usr/bin/python3
# -*- coding: utf-8 -*-

#autor: labruillere @ usual google mail dns
#date: 30/08/2017
#license: bsd


from os import listdir, sep, makedirs
from os.path import abspath, basename, isdir

def fileToArray(file_name):
	''' just open a file '''
	with open(file_name) as f:
		temp = f.readlines()
	return [x.strip("\n\r") for x in temp]

def arrayToFile(array, file_name):
	''' turn an array into a file '''
	try:
		with open(file_name, "w") as output:
			output.write("\n".join(array))
		return True
	except:
		print("unable to save the file '%s'" % file_name)

def create_dir(route):
	try:
		makedirs(route)
	except FileExistsError:
		pass

class Tree():
	'''
		return a list containing a tuple of:
		type, depth, name, route
	'''
	def __init__(self, folder):
		'''
			when initialised run _tree function and return a list of tuple
		
		'''
		self.list = []
		self._tree(folder)
		
	def _tree(self, directory, start = 0, appending = []):
		'''
			recursivly call himselft until all foders have been indexed
	
		'''
		appending_lenght = len(appending)
		depth = len(directory.split('/'))
		dir_basename = basename(directory)
		if start == 0:
			start += depth
			appending = [dir_basename]
		else:
			diff = depth - start
			if appending_lenght > diff:
				for i in range(appending_lenght-diff):
					appending.pop()
			appending.append(dir_basename)
	
		all_list = sorted(listdir(directory))
		files = []
		dirs = []
		for filename in all_list :
			path = directory + sep + filename
			if isdir(path) :
	 			dirs.append("" + filename)
			else:
				files.append("" + filename)
		depht = len(appending)-1
		#print("\t"*depht, appending[-1])
		self.list.append((0, 0+depht, appending[-1], "/".join(appending)))
		for filename in files :
			depth = len(appending)
			#print( "%s%s (%s/%s)" % ("\t"*depth, filename, "/".join(appending), filename))
			self.list.append((1, 0+depht, filename, "/".join(appending)))
			#print "\t" * diff, "-", filename
		for dirname in dirs :
			path = directory + sep + dirname
			self._tree(path, start,  appending)


	def print_list(self):
		for elem in self.list:
			if elem[0] == 0: #directory
				print("\t"*elem[1], elem[2])
			else:
				print("\t"*elem[1],"  ", elem[2])
