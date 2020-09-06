import sys

registers = ["eax", "ebx", "ecx", "edx", "ax", "ah", "al", "bx", "bh", "bl", "cx", "ch", "cl", "dx", "dh", "dl", "si", "di"]
builtins = ["inturrupt", "push_all", "pop_all", "hang"]
reserved = ["byte", "word", "dword", "string"]

def stripTabs(code):
	code = code.replace("\t", "")
	return code
	
def error(string, code):
	print(string)
	sys.exit(code)

def isReserved(string):
	if(string in registers or string in builtins or string in reserved):
		return True
	return False
