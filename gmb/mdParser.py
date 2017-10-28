#!/usr/bin/python3
# -*- coding: utf-8 -*-

#autor: labruillere @ usual google mail dns
#date: 30/08/2017
#license: bsd

from .fileToolz import fileToArray
import base64

class Parser :
	''' A simple markdown parser '''
	def __init__(self):
		''' init function '''
		self.verbose = 0
		self.markdown_array = []
		self.current_index = 0
		self.array_length = 0
		self.custom_js = []
		self.custom_css = []
		self.files_to_add = []
		self.result_html = []
		self.tabed = 0
		self.working_dir = ""
		self.line_jump = True
		self.disqus_id = ""
		
		self.allowedChars = ['_','-','.', ' ']
		
		self.monokeys = ["#","*","-","[","!", ">", "`"]
		self.monokey_option = {
			"#" : self.header,
			"*":self.puce,
			"-" : self.puce,
			"[":self.link,
			"!": self.image,
			">" : self.quote,
			"`":self.code
		}
		self.nestedkeys = ["*","_", "`", "~", "-", "["]
		self.nestedkey_option = {
			"*" : self.bold_or_italic_or_del_or_sub,
			"_"  : self.bold_or_italic_or_del_or_sub,
			"~" : self.bold_or_italic_or_del_or_sub,
			"-" : self.bold_or_italic_or_del_or_sub,
			"`" : self.inline_code,
			"[" : self.inline_link
		}
		
	def debug(self ,line ,level = 1):
		''' print the debug '''
		if self.verbose >= level or level < 0:
			print ("%s" % line)
	
	def yiel_disqus_html(self, PAGE_ID = ""):
		if type(self.disqus_id) is str and self.disqus_id != "":
			PAGE_URL = "window.location.href"
			#PAGE_URL = "'{{ page.url | replace:'index.html','' | prepend: site.baseurl | prepend: site.url }}'"
			result = ["<div id=\"disqus_thread\"></div><script>"]
			result += ["var disqus_config = function () {"]
			result += ["this.page.url = %s;" % PAGE_URL]
			result += ["this.page.identifier = '%s';" % PAGE_ID]
			result += ["};"]
			result += ["(function() { // DON'T EDIT BELOW THIS LINE"]
			result += ["var d = document, s = d.createElement('script');"]
			result += ["s.src = 'https://%s.disqus.com/embed.js';" % self.disqus_id]
			result += ["s.setAttribute('data-timestamp', +new Date());"]
			result += ["(d.head || d.body).appendChild(s);"]
			result += ["})();"]
			result += ["</script>"]
			result += ["<noscript>Please enable JavaScript to view the <a href=\"https://disqus.com/?ref_noscript\">comments powered by Disqus.</a></noscript>"]
			return result
		else:
			self.debug("you must set disqus id before using it", 1)
			return []
	def header(self, string) :
		length = len(string)
		if length > 6 and string[:6] == "######":
			result = "<div class=\"h6\">" + self.nestedParse(string[6:]) + "</div>"
		elif length > 5 and string[:5] == "#####":
			result = "<div class=\"h5\">" + self.nestedParse(string[5:]) + "</div>"
		elif length > 4 and string[:4] == "####":
			result = "<div class=\"h4\">" + self.nestedParse(string[4:]) + "</div>"
		elif length > 3 and string[:3] == "###":
			result = "<div class=\"h3\">" + self.nestedParse(string[3:]) + "</div>"
		elif length > 2 and string[:2] == "##":
			result = "<div class=\"h2\">" + self.nestedParse(string[2:]) + "</div>"
		else:
			result = "<div class=\"h1\">" + self.nestedParse(string[1:]) + "</div>"
		self.result_html += ["<div class=\"normal_element\">%s%s</div>" % (self.tabs(self.tabed), result)]
		self.current_index += 1
	
	def tabs(self,times) :
		self.debug("entering tabed",2)
		return "<div class=\"tabulation\">&nbsp;</div>"*times
	
	def puce(self, string) :
		self.debug("entering puce, with '%s'" % string, 2)
		if string[1] == " ":
			result = '<div class="puce">%s</div>' % self.nestedParse(string[2:]) 
		else:
			result = "<div class=\"normal_text\" >%s</div>" % self.nestedParse(string)
		self.result_html += ["<div class=\"normal_element\">%s%s</div>" % (self.tabs(self.tabed), result)]
		self.current_index += 1
	
	def link(self, string) :
		length = len(string)
		pointer = 2
		result = ""
		self.debug("%s%s%s" % (length, string[0], string[length-1]))
		if length < 6 or  string[length-1] != ")":
			self.debug("\terror invalid  link",-1)
			result += "<div class=\"normal_text\" >%s</div>" % self.nestedParse(string)
		else:
			found = False
			while pointer < length - 2:
				if  string[pointer] == "]" and string[pointer+1] == "(" :
					result += '<a target="_blank" class="link" href="%s">%s</a>' % (string[pointer+2:length-1], self.nestedParse(string[1:pointer]))
					found = True
				pointer += 1
			if not found:
				result += self.nestedParse(string)
		self.result_html += ["<div class=\"normal_element\">%s%s</div>" % (self.tabs(self.tabed), result)]
		self.current_index += 1
	
	def anormal_exit(self, string):
		self.debug(string,-1)
		exit(-1)
	
	def inline_link(self, string) :
		print(string)
		self.debug("\t\t --- Inside inline_link ---\n")
		name = ""
		link = ""
		pointer = 1
		mid_point = 1
		length = len(string)
		if length < 5:
			self.anormal_exit("invalid inline link, to small")
		while pointer < length :
			if string[pointer] == "]" and string[pointer - 1] != "\\":
				name += string[1:pointer-1]
				mid_point += pointer
				pointer += 1
				break
			pointer += 1
		print("step 1", string[pointer:])
		if string[pointer] != "(" or pointer == length:
			self.anormal_exit("invalid inline link, can't found (")
		while pointer < length :
			if string[pointer] == ")" and string[pointer - 1] != "\\":
				link += string[mid_point:pointer-1]
				pointer += 1
				break
			pointer +=1
		print("step 2", string[pointer:])
		if pointer == length:
			self.anormal_exit("invalid link, can't find )")
		self.debug("\t\t --- exiting inline link ---")
		return "<a href=\"%s\" >%s</a>%s" % (link,name,self.nestedParse(string[pointer:]))
	
	def image(self, string) :
		length = len(string)
		image_file  = ""
		pointer = 2
		result = ""
		self.debug("%s%s%s" % (length, string[0], string[length-1]))
		try:
			if length < 10 or string[1] != "[" or string[length-1] != ")":
				self.debug("\terror invalid image link",0)
				result += "<div class=\"normal_text\" >%s</div>" % self.nestedParse(string)
			else:
				while pointer < length - 2:
					if  string[pointer] == "]" and string[pointer+1] == "(" :
						image_file += string[pointer+2:length-1]
						if len(image_file) < 5:
							result += "<div class=\"normal_text\" >%s</div>" % self.nestedParse(string)
							break
						with open(self.working_dir + image_file, "rb") as f:
							encoded_string = base64.b64encode(f.read()).decode()
						result += '<img class="image" alt="%s" src="data:image/%s;base64,%s" />' % (string[2:pointer], image_file[-3] , encoded_string)
						break
					pointer += 1
			self.result_html += ["<div class=\"normal_element\">%s%s</div>" % (self.tabs(self.tabed), result)]
		except Exception as e:
			self.debug("!! unable to add image from markdown !!\n%s" % e,-1)
		self.current_index += 1
	
	def getNextLine(self):
		self.current_index  += 1
		if self.current_index  < self.array_length:
			return self.markdown_array[self.current_index]
		return None
	
	def function_normal_exit(self, result ):
		self.result_html += ["<div class=\"normal_element\">%s%s</div>" % (self.tabs(self.tabed), result)]
		self.current_index  += 1
	
	def quote(self,string) :
		result = ""
		result += '<div class="quote">%s' % self.nestedParse(string[1:])
		while True:
			tmp = self.getNextLine()
			if tmp != None and tmp != "":
				result += "</BR>%s" % self.nestedParse(tmp)
			else:
				break
		result += "</div>"
		self.function_normal_exit(result)
	
	def code(self, string) :
		self.debug("\t-- Entering code --\t'%s' and '%s'" % (string,string[-3:]), 1)
		length = len(string)
		result = ""
		if string[:3] != "```":
			self.debug("\terror invalid code string", 0)
			result += "<div class=\"normal_text\" >%s</div>" % self.nestedParse(string)
			self.function_normal_exit(result)
			return
		if length > 5 and string[-3:] == "```":
			self.debug("\t-- Exiting code  from oneline --", 1)
			result += '<pre><code class="language-none">%s</code></pre>' % string[3:-3]
			self.function_normal_exit(result)
			return
		if length == 3:
			self.debug("\t-- Exiting code  for simple code  --", 1)
			result +=  '<pre><code class="language-none">%s</code></pre>' % self.html_spacer(self.returnCodeLines())
			self.function_normal_exit(result)
			return
		if "```" in string[3:]:
			pos = string[3:].find("```")+3
			inside = string[3:pos]
			end = string[pos+3:]
			self.debug("\t\tinside code first : %s second : %s" % (inside, end) )
			result += '<div class=\"normal_text\" ><mark>%s</mark>%s</div>' % (self.nestedParse(inside),self.nestedParse(end))
			self.function_normal_exit(result)
			return
		typeofcode = self.sanityze(string[3:])
		self.debug("\t-- Exiting code  for %s code  --" % typeofcode, 1)
		if "```" in typeofcode:
			self.debug("-- should not endup here  --" , -1)
			quit()
		else:
			result += '<pre><code class="language-%s">%s</code></pre>'  % (typeofcode, self.html_spacer(self.returnCodeLines()) )
			self.function_normal_exit(result)
	
	def sanityze( self, string):
		result = ""
		if self.verbose > 1 :
			isalpha = False
			isnum = False
			isAllowed = False
			for elem in string:
				tmp = ord(elem)
				isalpha = (tmp > 96 and tmp < 123) or (tmp > 64 and tmp < 91)
				isnum = tmp > 47 and tmp < 58
				isAllowed = elem in self.allowedChars
				self.debug( elem, "ord is :", tmp, "is alpha :", isalpha, "is num :", isnum, "is allowed :", isAllowed)
				if isalpha or isnum or isAllowed : 
					result += elem
		else:
			for elem in string:
				tmp = ord(elem)
				if (tmp > 96 and tmp < 123) \
				or (tmp > 64 and tmp < 91)  \
				or (tmp > 47 and tmp < 58) \
				or (elem in self.allowedChars) : 
					result += elem
		return result
	
	def bold_or_italic_or_del_or_sub(self,string) :
		self.debug("\t\t --- Inside bold or italic ---\n")
		pointer = 1
		length = len(string)
		marker = string[0]
		double = False
		if length > 1 and string[1] == marker :
			if length < 5 :
				self.debug("\t\t\tError, invalid formed marker ( empty  ).",0)
				return string
			double = True
			pointer += 1
		while pointer < length :
			if string[pointer] == marker and string[pointer - 1] != "\\" :
				if double == True :
					if pointer + 1 < length and string[pointer + 1] == marker :
						add = "b"
						if marker == "~":
							add = "del"
						if marker == "-":
							add = "ins"
							print("|" + string[2:pointer].replace(" ", ".")+ "|\n|" +string[pointer+2:].replace(" ", ".") + "|")
						string = "<%s>%s</%s>%s"  % (add, self.nestedParse(string[2:pointer]), add, self.nestedParse(string[pointer+2:]))
						self.debug("\t\tBuielt string (double) : %s" % string ) 
						break
					self.debug("\t\t\tError, invalid formed marker ( not ending ) returnning string :%s " % string)
					return string
				else:
					string = "<i>" + self.nestedParse(string[1:pointer]) + "</i>" +  self.nestedParse(string[pointer+1:])
					self.debug("\t\t\tBuielt string (simple) : %s" % string )
					break
			pointer += 1
		if pointer == length :
			self.debug("\t\t\tError, invalid formed marker %s ( not ending)." % marker, 0)
		self.debug("\t\t --- exiting bold or italic ---")
		return string
	
	def inline_code(self, string) :
		self.debug("\t\t --- Inside inlinecode ---\n")
		pointer = 1
		length = len(string)
		while pointer < length :
			if string[pointer] == "`" and string[pointer - 1] != "\\" :
				string = "\t\t<mark>" + self.nestedParse(string[1:pointer]) + "</mark>" +  self.nestedParse(string[pointer+1:])
				self.debug("\t\t\tBuielt string (inline code) : %s" % string )
				break
			pointer += 1
		if pointer == length :
			self.debug("\t\t\tError, invalid formed marker %s ( not ending)." % marker, 0)
		self.debug("\t\t --- exiting inlinecode ---")
		return string
	
	def returnCodeLines(self):
		tmp = ""
		result = ""
		while tmp != None :
			tmp = self.getNextLine()
			if tmp != None:
				if len(tmp) == 3 and tmp[:3] == "```":
					return result
				result += "\n%s" % tmp
		return result
	
	def html_spacer(self, string):
		return string.replace("<", "< ")
	
	def nestedParse(self, string):
		if not string :
			return ""
		self.debug("\n\t--- entering nested ---")
		pointer = 0
		length = len(string)
		while pointer < length :
			if string[pointer] in self.nestedkeys :
				if pointer > 0 and string[pointer-1] == "\\" :
					continue
				if pointer + 2 >= length :
					self.debug("\t\tinvalid formed marker ( empty or not ending ) returnning string : %s" % string)
					self.debug("\n\t--- exiting nested ---")
					return string
				self.debug("\t\tfound start key : %s pos: %s " % ( str(string[pointer]), pointer ))
				break
			pointer += 1
		if pointer != length:
			string = string[:pointer] + self.nestedkey_option[string[pointer]](string[pointer:])
		else:
			self.debug("\t\tno key found in : %s" % string)
		self.debug("\t--- exiting nested ---")
		return string
	
	def first_parse(self, string):
		self.debug("doing first parse index:%s, length: %s" % (self.current_index, self.array_length))
		tmp = []
		pointer = 0
		self.tabed = 0
		length = len(string)
		while pointer < length and string[pointer] == "\t"  :
			pointer += 1
		self.tabed += pointer
		self.debug("\t%s%s" %( self.tabed ," tabs"))
		string = string[pointer:]
		if string != "" and string[0] in self.monokeys:
			self.debug("\tfound marker : %s executing ..." % string[0] )
			self.monokey_option[string[0]](string)
		else:
			self.debug("\tmarker not found, doing nested ..."  )
			if self.line_jump == True: 
				self.result_html += ["<div class=\"normal_element\">%s<div class=\"normal_text\" >%s</div></div>" % (self.tabs(self.tabed), self.nestedParse(string))]
			self.current_index += 1
		return tmp
		
	def parse(self, working_dir, file_name):
		''' a function that turn markdown array to html, return tuple ( html_array, js_files_to_add, css_files_to_add, (copy_type, files_to_copy_with) )'''
		self.markdown_array = fileToArray(working_dir + file_name)
		self.array_length = len(self.markdown_array)
		self.current_index = 0
		self.result_html = []
		self.custom_js = []
		self.custom_css = []
		self.files_to_add = []
		self.working_dir = "" + working_dir
		if self.markdown_array != []:
			self.debug("not empty file")
			while(self.current_index < self.array_length ):
				self.first_parse(self.markdown_array[self.current_index])
		else:
			self.debug("empty markdown")
		return (self.result_html,self.custom_js,self.custom_css,self.files_to_add)
