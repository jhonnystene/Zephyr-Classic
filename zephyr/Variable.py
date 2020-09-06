VARIABLE_TYPE_BYTE = 0
VARIABLE_TYPE_WORD = 1
VARIABLE_TYPE_DWORD = 2
VARIABLE_TYPE_STRING = 3

def createFrom(vartype, varname, varvalue, isGlobal):
	if(vartype == "byte"):
		vartype = VARIABLE_TYPE_BYTE
	elif(vartype == "word"):
		vartype = VARIABLE_TYPE_WORD
	elif(vartype == "dword"):
		vartype = VARIABLE_TYPE_DWORD
	elif(vartype == "string"):
		vartype = VARIABLE_TYPE_STRING
	
	v = Variable(vartype, varname, varvalue, isGlobal)
	return v

class Variable:
	def __init__(self, vartype, name, value, isGlobal):
		self.type = vartype
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
