import sys

registerNames = ["eax", "ebx", "ecx", "edx", "ax", "ah", "al", "bx", "bh", "bl", "cx", "ch", "cl", "dx", "dh", "dl", "si", "di"]
builtins = ["inturrupt", "push_all", "pop_all", "hang"]
def stripTabs(code):
	code = code.replace("\t", "")
	return code

class Function:
	def __init__(self, code, name):
		self.code = stripTabs(code) # Make sure we don't have any tabs messing up our code
		self.name = name # Set our function name
		
		# Parse function code into ASM
		# TODO: If/else statements, variables
		self.asm = ""
		for line in self.code.split("\n"):
			line = line[:-1] # Get rid of semicolon
			if(line.startswith("//") or line == ""): # Ignore empty lines and comments
				pass
			elif("=" in line): # Variable or register set
				varname = line.split(" ")[0].lower() # Get var/reg name
				varvalue = line.split(" ")[2] # Get desired value
				
				if(varname in registerNames): # Register?
					self.asm += "mov " + varname + ", " + varvalue + "\n"
				else: # Variable?
					print("Error in function \"" + self.name + "\": variables not supported yet!") # Not supported yet.
					sys.exit(3)
			elif("(" in line and ")" in line): # Function call
				command = line.split("(") # Split command and argument
				command[1] = command[1][:-1] # Remove ) from argument
				if(command[0] in builtins): # Are we trying to use a built-in function?
					if(command[0] == "inturrupt"): # INT?
						self.asm += "int " + command[1] + "\n"
					elif(command[0] == "push_all"): # PUSHA?
						self.asm += "pusha"
					elif(command[0] == "pop_all"): # POPA?
						self.asm += "popa"
					elif(command[0] == "hang"): # Hang?
						self.asm += ".hang:\njmp .hang"
				else: # Only call commands for now. Maybe JMP support in future?
					self.asm += "call " + command[0] + "\n"
			elif(line == "return"): # Returning from function?
				self.asm += "ret\n"
			else:
				print("Error in function code! (" + line + " invalid)") # TODO: Print line number
				sys.exit(3)
		
		# Check if function has return statement
		if("\nret\n" not in self.asm):
			print("Warning! Function \"" + self.name + "\" has no return!")

class SourceFile:
	# TODO: #include - Include a file
	
	def __init__(self, code):
		print("Parsing source code...")
		self.code = stripTabs(code) # Strip tabs
		self.functions = {} # Create function list
		self.mainFunction = ""
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
				
			# TODO global variables
				
			elif("{" in code[line]): # Starting a function?
				if("func" in code[line]):
					# Sort out the name from the code and store it in a new Function object
					func = ""
					funcName = code[line].split(" ")[1]
					cLine = ""
					while("}" not in cLine):
						func += cLine
						line += 1
						cLine = code[line] + "\n"
						
					func = Function(func, funcName)
					self.functions[funcName] = func
				else:
					print("Error on line " + str(line + 1) + ": Misplaced '{'")
					sys.exit(3)
			else:
				print("Error on line " + str(line + 1) + ": Misplaced non-function code.")
				sys.exit(3)
			line += 1
		
		print("Found " + str(len(self.functions)) + " functions.")
				
	def genASM(self):
		if(self.mainFunction == ""):
			print("Error! Program does not contain a #mainfunc preprocessor instruction.")
			sys.exit(4)
		
		asm = ""
		
		asm += "call " + self.mainFunction + "\n" # Add main function call
		
		# Add function source codes
		for function in self.functions:
			asm += function[:-2] + ":\n"
			asm += self.functions[function].asm
			
		return asm
