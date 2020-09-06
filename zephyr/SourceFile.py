import zephyr
from zephyr import Function, Variable

def createFrom(code):
	sf = SourceFile()
	sf.code = code
	sf.parse()
	return sf

class SourceFile:
	# TODO: #include - Include a file
	
	def __init__(self):
		self.code = ""
		self.functions = {}
		self.variables = []
		self.mainFunction = ""
	
	def parse(self):
		print("Parsing source code...")
		self.code = zephyr.stripTabs(self.code) # Strip tabs
		code = self.code.split("\n") # Split up into newlines so we can loop through
		
		# Not a for loop because we're about to jump all over the place
		line = 0
		while(line != len(code)):
			if(code[line].startswith("//") or code[line] == ""): # Comment or empty line?
				pass # Ignore it
				
			elif(code[line].startswith("#")): # Preprocessor instruction
				instruction = code[line][1:].split(" ")
				if(instruction[0] == "mainfunc"):
					self.mainFunction = instruction[1]
					
				elif(instruction[0] == "global"):
					vartype = instruction[1]
					varname = instruction[2]
					if(varname in zephyr.registers or varname in zephyr.builtins):
						zephyr.error("Error! " + varname + " is reserved.", 5);
					if(len(instruction) == 5):
						varvalue = instruction[4]
					else:
						varvalue = ""
						for i in range(4, len(instruction)):
							varvalue += instruction[i] + " "
					
					if(vartype == "byte"):
						vartype = Variable.VARIABLE_TYPE_BYTE
					elif(vartype == "word"):
						vartype = Variable.VARIABLE_TYPE_WORD
					elif(vartype == "dword"):
						vartype = Variable.VARIABLE_TYPE_DWORD
					elif(vartype == "string"):
						vartype = Variable.VARIABLE_TYPE_STRING
						
					self.variables.append(Variable.createFrom(vartype, varname, varvalue, True))
					
			elif("{" in code[line]): # Starting a function?
				if("func" in code[line]):
					# Sort out the name from the code and store it in a new Function object
					func = ""
					funcName = code[line].split(" ")[1]
					if(funcName in zephyr.registers or funcName in zephyr.builtins):
						zephyr.error("Error! " + funcName + " is reserved.", 5);
					cLine = ""
					while("}" not in cLine):
						func += cLine
						line += 1
						cLine = code[line] + "\n"
						
					func = Function.createFrom(func, funcName)
					self.functions[funcName] = func
				else:
					zephyr.error("Error on line " + str(line + 1) + ": Misplaced '{'", 3)
			else:
				zephyr.error("Error on line " + str(line + 1) + ": Misplaced non-function code.", 3)
			line += 1
		
		print("Found " + str(len(self.functions)) + " functions.")
				
	def genASM(self):
		if(self.mainFunction == ""):
			zephyr.error("Error! Program does not contain a #mainfunc preprocessor instruction.", 4)
		
		asm = "call " + self.mainFunction + "\n" # Start with main function call
		
		# Add function source codes
		for function in self.functions:
			asm += function[:-2] + ":\n"
			asm += self.functions[function].genASM()
			
		# Don't try to run global variables
		asm += "hang:\njmp hang\n"
		
		# Add global variables
		for variable in self.variables:
			asm += variable.genASM() + "\n"
			
		return asm
