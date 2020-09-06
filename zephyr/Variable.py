VARIABLE_TYPE_BYTE = 0
VARIABLE_TYPE_WORD = 1
VARIABLE_TYPE_DWORD = 2
VARIABLE_TYPE_STRING = 3

def createFrom(variableType, variableName, variableValue, isGlobal):
	if(variableType == "byte"):
		variableType = VARIABLE_TYPE_BYTE
	elif(variableType == "word"):
		variableType = VARIABLE_TYPE_WORD
	elif(variableType == "dword"):
		variableType = VARIABLE_TYPE_DWORD
	elif(variableType == "string"):
		variableType = VARIABLE_TYPE_STRING
	
	v = Variable(variableType, variableName, variableValue, isGlobal)
	return v

class Variable:
	def __init__(self, variableType, name, value, isGlobal):
		self.type = variableType
		self.name = name.lower()
		self.value = value
		self.isGlobal = isGlobal
	
	def genASM(self):
		if(self.isGlobal):
			asm = self.name
		else:
			asm = "." + self.name
			
		if(self.type == VARIABLE_TYPE_BYTE or self.type == VARIABLE_TYPE_STRING):
			asm += " db "
		elif(self.type == VARIABLE_TYPE_WORD):
			asm += " dw "
		elif(self.type == VARIABLE_TYPE_DWORD):
			asm += " dd "
		else:
			print("Invalid type " + str(self.type) + " on variable " + self.name)
			sys.exit(3)
		
		if(self.type == VARIABLE_TYPE_STRING):
			self.value = self.value.replace("\n", "\", 13, 10, \"")
			
		asm += self.value
		
		if(self.type == VARIABLE_TYPE_STRING):
			asm += ", 0"
		
		return asm
