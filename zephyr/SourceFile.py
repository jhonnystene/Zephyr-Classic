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
		while(line < len(code)):
			# Ignore comments and empty lines
			if(code[line].startswith("//") or code[line] == ""):
				pass
				
			# Handle preprocessor instructions
			elif(code[line].startswith("#")):
				instruction = code[line][1:].split(" ")
				
				# Set main function
				if(instruction[0] == "mainfunc"):
					self.mainFunction = instruction[1]
					
				# Create global variable
				elif(instruction[0] == "global"):
					variableType = instruction[1]
					variableName = instruction[2]
					
					# Make sure we're not trying to use a reserved name
					if(zephyr.isReserved(variableName)):
						zephyr.error("Error! " + variableName + " is reserved.", 5);
					
					# Make sure we treat everything after the variable name as one argument
					if(len(instruction) == 5):
						variableValue = instruction[4]
					else:
						variableValue = ""
						for i in range(4, len(instruction)):
							variableValue += instruction[i] + " "

					# Create a new variable object and add it to our list
					self.variables.append(Variable.createFrom(variableType, variableName, variableValue, True))
					
			# New function
			elif("func " in code[line]):
				# Make sure we don't try to interpret curly brackets on other lines
				if("{" not in code[line]):
					line += 1
				
				# Init variables
				functionCode = ""
				functionName = code[line].split(" ")[1]
				
				# Make sure we're not trying to use a reserved name
				if(zephyr.isReserved(functionName)):
					zephyr.error("Error! " + functionName + " is reserved.", 5);
					
				# Loop through the code and add it to the function code
				currentLine = ""
				while("}" not in currentLine):
					functionCode += currentLine
					line += 1
					currentLine = code[line] + "\n"
				
				# Create a Function object from the code and store it in our function list
				function = Function.createFrom(functionCode, functionName)
				self.functions[functionName] = function
			
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
