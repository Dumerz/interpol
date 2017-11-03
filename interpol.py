# Filename		: Interpol.py
# Author		: Zremud
# Year			: 2017
# Description	: simple integer oriented programming language that deals with integers with no floating-point values.

import re

# [class] Defining Interpol Class
class Interpol:

	# [var] declared for Interpol expression to be executed
	expression = ""
	sectionList = ""

	# [var] (list) keywords of interpol
	keywords = ['CREATE', 'RUPTURE', 'DINT', 'DSTR', 'WITH', 'GIVEME?', 'GIVEYOU!', 'GIVEYOU!!', 'STORE', 'IN', 'PLUS', 'MINUS', 'TIMES', 'DIVBY', 'MODU', 'RAISE', 'ROOT', 'MEAN', 'DIST', 'AND']
	operations = ['PLUS', 'MINUS', 'TIMES', 'DIVBY', 'MODU', 'RAISE', 'ROOT', 'MEAN', 'DIST']
	enders = ['RUPTURE', 'DINT', 'DSTR', 'GIVEME?', 'GIVEYOU!', 'GIVEYOU!!', 'STORE', 'IN']
	starters = ['WITH', 'DINT', 'DSTR', 'GIVEME?', 'GIVEYOU!', 'GIVEYOU!!', 'STORE', 'IN']
	
	# [func] initialize the [class] Interpol, trigerred if new instance [class] Interpol is created
	def __init__(self):
		self.print_header()
		self.get_input()

	# [func] print the interpreter header
	def print_header(self):
		print('INTERPOL Interpreter v0.1 (v0.1, Oct 24 2017)')
		print('The section should be between "CREATE" and "RUPTURE" keywords.')
		print('Press [CTRL] + [C] to exit interpreter.')

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
					content = re.sub("\[[^]]*\]", lambda x:x.group(0).replace(' ','~'), content)
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
			self.handle_error_pos('Invalid start of section at \'' + self.sectionList[0] + '\'', 0)
		elif not self.is_valid_end(self.sectionList, len(self.sectionList)-1): # refer to [func] is_valid_end
			self.handle_error_pos('Invalid end of section at \'' + self.sectionList[len(self.sectionList)-1] +  '\'',len(self.sectionList)-1)
		else: # Traverse all the codes in the statement
			now_token = 1
			now_var = []
			var_names = []
			var = {}

			while True:
				if now_token >= len(self.sectionList)-1: break # Test if the [var] now_token is the last to test; if true break
				else: #now_token is NOT the last
					if self.is_valid_start_end(now_token): # refer to [func] is_valid_start_end
						break
					elif self.sectionList[now_token] in self.starters:
						if self.is_dint(self.sectionList[now_token]):
							if self.is_valid_varname(self.sectionList[now_token + 1], now_token + 1):
								if not self.sectionList[now_token + 1] in var_names:
									now_var = ['INT', self.sectionList[now_token + 1]]
									var_names.append(self.sectionList[now_token + 1])
									var[now_var[1]] =  0
									now_token = now_token + 2
								else:
									self.handle_error_pos('Invalid var_name \'' + self.sectionList[now_token + 1] + '\' already used', now_token + 1)
									break
							else:
								break
						elif self.is_dstr(self.sectionList[now_token]):
							if self.is_valid_varname(self.sectionList[now_token + 1], now_token + 1):
								if not self.sectionList[now_token + 1] in var_names:
									now_var = ['STRING', self.sectionList[now_token + 1]]
									var_names.append(self.sectionList[now_token + 1])
									var[now_var[1]] =  ''
									now_token = now_token + 2
								else:
									self.handle_error_pos('Invalid var_name \'' + self.sectionList[now_token + 1] + '\' already used', now_token + 1)
									break
							else:
								break
						elif self.is_with(self.sectionList[now_token]):
							if now_var == []:
								self.handle_error_pos('Invalid token \'' + self.sectionList[now_token] + '\'', now_token)
								break
							elif now_var[0] == 'INT':
								if self.sectionList[now_token + 1].isdigit():
									var[now_var[1]] =  int(self.sectionList[now_token + 1])
									now_token = now_token + 2
									now_var = []
								elif self.sectionList[now_token + 1] in self.operations:
									var[now_var[1]] = self.evaluate(now_token+1, var_names, var)
									now_token = self.get_next_starter(now_token+1)
								else:
									self.handle_error_pos('Invalid value \'' + self.sectionList[now_token + 1] + '\'', now_token)
									break
							elif now_var[0] == 'STRING':
								if self.sectionList[now_token + 1].startswith('['):
									if self.sectionList[now_token + 1].endswith(']'):
										var[now_var[1]] =  self.sectionList[now_token + 1].strip('[]').replace('~',' ')
										now_var = []
										now_token = now_token + 2
									else:
										self.handle_error_pos('Invalid value \'' + self.sectionList[now_token + 1] + '\'', now_token)
										break
								else:
									self.handle_error_pos('Invalid value \'' + self.sectionList[now_token + 1] + '\'', now_token)
									break
						elif self.is_store(self.sectionList[now_token]):
							if self.sectionList[now_token + 1].isdigit():
								now_var = ['INT', self.sectionList[now_token + 1]]
								now_token = now_token + 2
							elif self.sectionList[now_token + 1] in self.operations:
								now_var = ['INT', self.evaluate(now_token+1, var_names, var)]
								now_token = self.get_next_starter(now_token+1)
							elif self.sectionList[now_token + 1].startswith('['):
								if self.sectionList[now_token + 1].endswith(']'):
									now_var = ['STRING', self.sectionList[now_token + 1].strip('[]').replace('~',' ')]
									now_token = now_token + 2
								else:
									self.handle_error_pos('Invalid value \'' + self.sectionList[now_token + 1] + '\'', now_token)
									break
							else:
								self.handle_error_pos('Invalid value \'' + self.sectionList[now_token + 1] + '\'', now_token)
								break

						elif self.is_in(self.sectionList[now_token]):
							if self.sectionList[now_token+1] in var_names:
								if now_var == []:
									self.handle_error_pos('Invalid token \'' + self.sectionList[now_token+1] + '\'', now_token + 1)
									break
								if str(now_var[1]).isdigit():
									if now_var[0] == 'INT':
										var[self.sectionList[now_token+1]] =  int(now_var[1])
										now_token = now_token + 2
										now_var = []
									else:
										self.handle_error_pos('Invalid value \'' + self.sectionList[now_token+1] + '\' type mismatch', now_token+1)
										break
								else:
									if now_var[0] == 'STRING':
										if not str(var[self.sectionList[now_token+1]]).isdigit():
											var[self.sectionList[now_token+1]] =  now_var[1].strip('[]').replace('~',' ')
											now_var = []
											now_token = now_token + 2
										else:
											self.handle_error_pos('Invalid value \'' + self.sectionList[now_token+1] + '\' type mismatch', now_token+1)
											break	
									else:
										self.handle_error_pos('Invalid value \'' + self.sectionList[now_token+1] + '\' type mismatch', now_token+1)
										break
							else:
								self.handle_error_pos('Invalid token \'' + self.sectionList[now_token+1] + '\'', now_token)
								break

						elif self.is_giveme(self.sectionList[now_token]):
							if self.sectionList[now_token+1] in var_names:
								value = raw_input()
								if isinstance(var[self.sectionList[now_token+1]], int):
									if value.isdigit():
										value = int(value)
									else:
										self.handle_error_pos('Invalid value \'' + self.sectionList[now_token+1] + '\' type mismatch', now_token+1)
										break
								var[self.sectionList[now_token+1]] = value
								now_token = now_token + 2
							else:
								self.handle_error_pos('Invalid variable \'' + self.sectionList[now_token+1] + '\' is not declared', now_token+1)
								break

						elif self.is_giveyou1(self.sectionList[now_token]):
							if self.sectionList[now_token+1] in var_names:
								print var[self.sectionList[now_token+1]]
								now_token = now_token + 2
							elif self.sectionList[now_token+1] in self.operations:
								print self.evaluate(int(now_token+1), var_names, var)
								now_token = self.get_next_starter(now_token+1)
							elif self.sectionList[now_token + 1].startswith('['): # value dapat
								if self.sectionList[now_token + 1].endswith(']'):
									print self.sectionList[now_token+1].strip('[]').replace('~',' ')
									now_token = now_token + 2
							elif self.sectionList[now_token+1].isdigit(): # value dapat
									print self.sectionList[now_token+1]
									now_token = now_token + 2
							else:
								self.handle_error_pos('Invalid token \'' + self.sectionList[now_token+1] + '\'', now_token)
								break

						elif self.is_giveyou2(self.sectionList[now_token]):
							if self.sectionList[now_token+1] in var_names:
								print str(var[self.sectionList[now_token+1]]) + '\n'
								now_token = now_token + 2
							elif self.sectionList[now_token+1] in self.operations:
								print self.evaluate(int(now_token+1), var_names, var)
								now_token = self.get_next_starter(now_token+1)
							elif self.sectionList[now_token + 1].startswith('['): # value dapat
								if self.sectionList[now_token + 1].endswith(']'):
									print str(self.sectionList[now_token+1].strip('[]').replace('~',' ')) + '\n'
									now_token = now_token + 2
							elif self.sectionList[now_token+1].isdigit(): # value dapat
									print str(self.sectionList[now_token+1]) + '\n'
									now_token = now_token + 2
							else:
								self.handle_error_pos('Invalid token \'' + self.sectionList[now_token+1] + '\'', now_token)
								break
						else:
							break
					else:
						self.handle_error_pos('Invalid token \'' + self.sectionList[now_token] + '\'', now_token)
						break

	def get_next_starter(self, pos):
		while True:
			if not self.sectionList[pos] in self.enders:
				pos = pos + 1
			else:
				break
		return pos

	def get_operations(self, pos):
		operations = []
		while True:
			if not self.sectionList[pos] in self.enders:
				operations.append(self.sectionList[pos])
				pos = pos + 1
			else:
				break
		return operations

	# [func] evaluate
	def evaluate(self, pos, var_names, var):
		OprStack = []
		Operations = self.get_operations(pos)
		for t in reversed(Operations):
			pos = pos + 1
			if t == 'PLUS':
				if len(OprStack) == 2:
					OprStack[-2:] = [int(OprStack[-1]) + int(OprStack[-2])]
				else:
					self.handle_error_pos('Arithmetic error occured \'' + t + '\'', pos)
					break
			elif t == 'MINUS':
				if len(OprStack) == 2:
					OprStack[-2:] = [int(OprStack[-1]) - int(OprStack[-2])]
				else:
					self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
					break
			elif t == 'TIMES':
				if len(OprStack) == 2:
					OprStack[-2:] = [int(OprStack[-1]) * int(OprStack[-2])]
				else:
					self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
					break
			elif t == 'DIVBY':
				if len(OprStack) == 2:
					if not int(OprStack[-2]) == 0:
						OprStack[-2:] = [int(OprStack[-1]) / int(OprStack[-2])]
					else:
						self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
						break
				else:
					self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
					break
			elif t == 'RAISE':
				if len(OprStack) == 2:
					OprStack[-2:] = [int(OprStack[-1]) ** int(OprStack[-2])]
				else:
					self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
					break
			elif t == 'ROOT':
				if len(OprStack) == 2:
					OprStack[-2:] = [int(OprStack[-2]) ** (1 / float(OprStack[-1]))]
				else:
					self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
					break
			elif t == 'MODU':
				if len(OprStack) == 2:
					if not int(OprStack[-2]) == 0:
						OprStack[-2:] = [int(OprStack[-1]) % int(OprStack[-2])]
					else:
						self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
						break
				else:
					self.handle_error_pos('Arithmetic error occured at \'' + t + '\'', pos)
					break
			elif t == 'MEAN':
				OprStack[-2:] = [self.get_mean(OprStack)]
			elif t in var_names:
				if str(var[t]).isdigit():
					OprStack.append(int(var[t]))
				else:
					self.handle_error_pos('Invalid token \'' + t + '\'', pos)
					break
			elif not str(t).isdigit():
				self.handle_error_pos('Invalid token \'' + t + '\'', pos)
				break
			else: OprStack.append(t)
		if not OprStack == []:
			return OprStack[0]

	def get_mean(self, OprStack):
	    pos = 0
	    Ans = 0
	    length = len(OprStack) - 1
	    for i in OprStack:
	        if pos < length:
	            Ans += int(OprStack[pos])
	        pos += 1
	    return Ans / length

	# [func] (return Boolean) test if [var] token is CREATE or RUPTURE
	def is_valid_start_end(self, token): # [param] token -> current token
		if self.is_valid_start(self.sectionList, token): # refer to [func] is_valid_start
			self.handle_error_pos('\'' + self.sectionList[token] + '\' should only be on the start of the section', token)
			return True
		elif self.is_valid_end(self.sectionList, token):# refer to [func] is_valid_end
			self.handle_error_pos('\'' + self.sectionList[token] + '\' should only be on the end of the section', token)
			return True
		else: #token is NOT token is CREATE or RUPTURE
			return False

	# [func] (return Boolean) test if the start of section is valid
	def is_valid_start(self, token, pos):	# [param] (token) token to be tested 
		if token[pos] == self.keywords[0]:
			return True
		else:
			return False

	# [func] (return Boolean) test if the end of section is valid
	def is_valid_end(self, token, pos):	# [param] (token) section to be tested 
		if token[pos] == self.keywords[1]:
			return True
		else:
			return False

	# [func] (return Boolean) test if declare of int
	def is_dint(self, entry):
		if entry == self.keywords[2]:
			return True
		else:
			return False

	# [func] (return Boolean) test if store
	def is_store(self, entry):
		if entry == self.keywords[8]:
			return True
		else:
			return False

	# [func] (return Boolean) test if in
	def is_in(self, entry):
		if entry == self.keywords[9]:
			return True
		else:
			return False

	# [func] (return Boolean) test if declare of str
	def is_dstr(self, entry):
		if entry == self.keywords[3]:
			return True
		else:
			return False

	# [func] (return Boolean) test if declare with value
	def is_with(self, entry):
		if entry == self.keywords[4]:
			return True
		else:
			return False

	# [func] (return Boolean) test if giveme
	def is_giveme(self, entry):
		if entry == self.keywords[5]:
			return True
		else:
			return False

	# [func] (return Boolean) test if giveyou
	def is_giveyou1(self, entry):
		if entry == self.keywords[6]:
			return True
		else:
			return False

	# [func] (return Boolean) test if declare of int valid
	def is_giveyou2(self, entry):
		if entry == self.keywords[7]:
			return True
		else:
			return False

	# [func] (return Boolean) test if var_name is valid
	def is_valid_varname(self, token, pos):
		if token in self.keywords:
			self.handle_error_pos('Invalid var_name \'' + token + '\'', pos)
			return False
		else:
			return True		

	# [func] handle exceptions
	def handle_error(self, msg): # [param] (msg) message to be printed 
		print('Error: ' + msg)

	# [func] handle exceptions
	def handle_error_pos(self, msg, pos): # [param] (msg) message to be printed 
		print('Error: [token ' + str(pos + 1) + '] ' + msg)

# New instance of [class] Interpol is created
# [func] Interpol.__init__ will be automatically triggered
interpol = Interpol()
