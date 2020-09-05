def stripTabs(code):
	code = code.replace("\t", "")
	return code

class Function:
	def __init__(self, code):
		self.code = stripTabs(code)
		self.asm = ""
		for line in self.code.split("\n"):
			print(line)

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
						
					func = Function(func)
					self.functions[funcName] = func
					
				else:
					print("Error on line " + str(line + 1) + ": Misplaced '{'")
					sys.exit(3)
			else:
				print("Error on line " + str(line + 1) + ": Misplaced non-function code.")
				sys.exit(3)
			line += 1
		
		print("Found " + str(len(self.functions)) + " functions.")
				
		
