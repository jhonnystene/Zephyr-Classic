import sys

registers = ["eax", "ebx", "ecx", "edx", "ax", "ah", "al", "bx", "bh", "bl", "cx", "ch", "cl", "dx", "dh", "dl", "si", "di"]
builtins = ["inturrupt", "push_all", "pop_all", "hang"]

def stripTabs(code):
	code = code.replace("\t", "")
	return code
	
def error(string, code):
	print(string)
	sys.exit(code)
