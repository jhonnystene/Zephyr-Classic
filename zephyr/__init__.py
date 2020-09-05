import sys

registerNames = ["eax", "ebx", "ecx", "edx", "ax", "ah", "al", "bx", "bh", "bl", "cx", "ch", "cl", "dx", "dh", "dl", "si", "di"]
builtins = ["inturrupt"]
def stripTabs(code):
	code = code.replace("\t", "")
	return code

class Function:
	def __init__(self, code, name):
		self.code = stripTabs(code)
		self.name = name
		self.asm = ""
		for line in self.code.split("\n"):
			line = line[:-1]
			if(line.startswith("//") or line == ""):
				pass
			elif("=" in line): # Variable or register set
				varname = line.split(" ")[0].lower()
				varvalue = line.split(" ")[2]
				if(varname in registerNames):
					self.asm += "mov " + varname + ", " + varvalue + "\n"
				else:
					print("Error in function \"" + self.name + "\": variables not supported yet!")
					sys.exit(3)
			elif("(" in line and ")" in line): # Function call
				command = line.split("(")
				command[1] = command[1][:-1]
				if(command[0] in builtins):
					if(command[0] == "inturrupt"):
						self.asm += "int " + command[1] + "\n"
				else:
					self.asm += "call " + command[0] + "\n"
			elif(line == "return"):
				self.asm += "ret\n"
			else:
				print("Error in function code! (" + line + " invalid)") # TODO: Print line number
				sys.exit(3)
		if("\nret\n" not in self.asm):
			print("Warning! Function \"" + self.name + "\" has no return!")

class SourceFile:
	def __init__(self, code):
		print("Parsing source code...")
		self.code = stripTabs(code)
		self.functions = {}
		code = self.code.split("\n")
		line = 0
		
		while(line != len(code)):
			if(code[line].startswith("//") or code[line] == ""): # Comment or empty line?
				pass # Ignore it
				
			# TODO global variables
				
			elif("{" in code[line]): # Starting a function?
				if("func" in code[line]):
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
				
		
