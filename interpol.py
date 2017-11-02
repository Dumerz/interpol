# Filename		: Interpol.py
# Author		: Zremud
# Year			: 2017
# Description	: simple integer oriented programming language that deals with integers with no floating-point values.

# [class] Defining Interpol Class
class Interpol:

	# [var] declared for Interpol expression to be executed
	expression = ""
	sectionList = ""

	# [var] (list) keywords of interpol
	keywords = ['CREATE', 'RUPTURE', 'DINT', 'DSTR', 'WITH', 'GIVEME?', 'GIVEYOU!', 'GIVEYOU!!', 'STORE', 'IN', 'PLUS', 'MINUS', 'TIMES', 'DIVBY', 'MODU', 'RAISE', 'ROOT', 'MEAN', 'DIST']
	prim_keywords = ['DINT', 'DSTR', 'GIVEME?', 'GIVEYOU!', 'GIVEYOU!!', 'STORE', 'PLUS', 'MINUS', 'TIMES', 'DIVBY', 'MODU', 'RAISE', 'ROOT', 'MEAN', 'DIST']
	
	# [func] initialize the [class] Interpol, trigerred if new instance [class] Interpol is created
	def __init__(self):
		self.print_header()
		self.get_input()

	# [func] print the interpreter header
	def print_header(self):
		print('INTERPOL Interpreter v0.1 (v0.1, Oct 24 2017)')
		print('The section should be between "CREATE" and "RUPTURE" keywords.')

	# [func] get user input on console
	def get_input(self):
		while True:
			self.expression = ""
			self.sectionList = ""
			file_name = raw_input('Enter the filename of the code to be executed: ') # get file_name of code to be executed
			if file_name.endswith('.ipol'): # test if file_name has .ipol extension
				try: # try if the requested file_name exists
					file = open(file_name)
					content = file.read()
					self.expression = content.strip()	# [str func] Multiple whitespaces and tabs are removed
					self.sectionList = self.expression.split()
					self.interpret_code()	# refer to [func] interpret_code
				except IOError:
					self.handle_error('No such file: ' + file_name + ' was found');
			else:
				self.handle_error('Invalid file type: ' + file_name + ' should be *.ipol')

	# [func] this is the main logic of the Interpol interpreter
	def interpret_code(self):
		if  self.sectionList == []: # test if section is null
			self.handle_error('Invalid start of section')
		elif not self.is_valid_start(self.sectionList, 0): # refer to [func] is_valid_start
			self.handle_error('Invalid start of section at ' + self.sectionList[0])
		elif not self.is_valid_end(self.sectionList, len(self.sectionList)-1): # refer to [func] is_valid_end
			self.handle_error('Invalid end of section at ' + self.sectionList[len(self.sectionList)-1])
		else:	# Traverse all the codes in the statement
			current_code = 1
			while True:
				if current_code >= len(self.sectionList)-1: break # Test if the [var] current_code is the last to test; if true break
				else:
					if self.is_valid_start(self.sectionList, current_code): # refer to [func] is_valid_start
						self.handle_error(self.sectionList[current_code] + ' should only be on the start of the section')
						break
					elif self.is_valid_end(self.sectionList, current_code):# refer to [func] is_valid_end
						self.handle_error(self.sectionList[current_code] + ' should only be on the end of the section')
						break
					elif current_code == 1:
						pass # if self.sectionList[current_code] in self.prim_keywords 
					print(self.sectionList[current_code])
					current_code = current_code + 1

	# [func] (return Boolean) test if the start of section is valid
	def is_valid_start(self, section, pos):	# [param] (section) section to be tested 
		if section[pos] == self.keywords[0]:
			return True
		else:
			return False

	# [func] (return Boolean) test if the end of section is valid
	def is_valid_end(self, section, pos):	# [param] (section) section to be tested 
		if section[pos] == self.keywords[1]:
			return True
		else:
			return False

	# [func] (return Boolean) test if declare of int valid
	def is_valid_dint(self, entry):
		if entry == self.keywords[2]:
			return True
		else:
			return False

	# [func] (return Boolean) test if var_name is valid
	def is_valid_varname(self, entry):
		if entry in keywords:
			return False
		else:
			return True		

	# [func] handle exceptions
	def handle_error(self, msg): # [param] (msg) message to be printed 
		print(msg)

# New instance of [class] Interpol is created
# [func] Interpol.__init__ will be automatically triggered
interpol = Interpol()
