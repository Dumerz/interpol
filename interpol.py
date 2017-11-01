# Filename		: Interpol.py
# Author		: Zremud
# Year			: 2017
# Description	: simple integer oriented programming language that deals with integers with no floating-point values.

# [class] Defining Interpol Class
class Interpol:

	# [var] declared for Interpol expression to be executed
	expression = ""

	# [var] (list) keywords of interpol
	keywords = ['CREATE', 'RUPTURE', 'DINT', 'DSTR', 'WITH', 'GIVEME?', 'GIVEYOU!', 'GIVEYOU!!', 'STORE', 'PLUS', 'MINUS', 'TIMES', 'DIVBY', 'MODU', 'RAISE', 'ROOT', 'MEAN', 'DIST']

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
			file_name = raw_input('Enter the filename of the code to be executed: ')
			file = open(file_name)
			content = file.read()
			self.expression = content.rstrip()	# [str func] Multiple whitespaces and tabs are removed
			print(self.expression.split(' '))
			if not self.is_valid_start(self.expression):
				self.handle_error('Invalid start of section')
			if not self.is_valid_end(self.expression):
				self.handle_error('Invalid end of section')

	# [func] (return Boolean) test if the start of section is valid
	def is_valid_start(self, section):	# [param] (section) section to be tested 
		return section.startswith(self.keywords[0])

	# [func] (return Boolean) test if the end of section is valid
	def is_valid_end(self, section):	# [param] (section) section to be tested 
		return section.endswith(self.keywords[1])

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
