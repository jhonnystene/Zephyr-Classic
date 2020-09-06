import zephyr
from zephyr import Variable

def createFrom(code, name):
	f = Function()
	f.code = code
	f.name = name
	f.genASM()
	return f

class Function:
	def __init__(self):
		self.code = ""
		self.name = ""
		self.variables = []
		
	def genASM(self):
		# Parse function code into ASM
		# TODO: If/else statements, for loops, while loops
		asm = ""
		
		for line in self.code.split("\n"):
			line = line[:-1] # Get rid of semicolon
			if(line.startswith("//") or line == ""): # Ignore empty lines and comments
				pass
			elif(" = " in line): # Variable or register set
				if("byte " in line or "word " in line or "dword " in line or "string " in line):
					vartype = line.split(" ")[0]
					varname = line.split(" ")[1].lower()
					if(varname in zephyr.registerNames or varname in zephyr.builtins):
						zephyr.error("Error! " + varname + " is reserved.", 5);
					if(len(line.split(" ")) == 4):
						varvalue = line.split(" ")[3]
					else:
						varvalue = ""
						for i in range(3, len(line.split(" "))):
							varvalue += line.split(" ")[i] + " "
						
					self.variables.append(Variable.createFrom(vartype, varname, varvalue, False))
				else:
					varname = line.split(" ")[0].lower() # Get var/reg name
					varvalue = line.split(" ")[2].lower() # Get desired value
					
					# Local or global variable?
					for variable in self.variables:
						if(varname == variable.name):
							varname = "." + varname	
					
					asm += "mov " + varname + ", " + varvalue + "\n"
						
			elif("+=" in line or "-=" in line): # Math
				instruction = line.split(" ")
				if(instruction[1] == "+="):
					asm += "add " + instruction[0].lower() + ", " + instruction[2].lower() + "\n"
				else:
					asm += "sub " + instruction[0].lower() + ", " + instruction[2].lower() + "\n"
				
			elif("(" in line and ")" in line): # Function call
				command = line.split("(") # Split command and argument
				command[1] = command[1][:-1] # Remove ) from argument
				if(command[0] in zephyr.builtins): # Are we trying to use a built-in function?
					if(command[0] == "inturrupt"): # INT?
						asm += "int " + command[1] + "\n"
					elif(command[0] == "push_all"): # PUSHA?
						asm += "pusha"
					elif(command[0] == "pop_all"): # POPA?
						asm += "popa"
					elif(command[0] == "hang"): # Hang?
						asm += ".hang:\njmp .hang\n"
				else: # Only call commands for now. Maybe JMP support in future?
					asm += "call " + command[0] + "\n"
			elif(line == "return"): # Returning from function?
				asm += "ret\n"
			else:
				zephyr.error("Error in function code! (" + line + " invalid)", 3) # TODO: Print line number
		
		for variable in self.variables:
			asm += variable.genASM() + "\n"
		
		# Check if function has return statement
		if("\nret\n" not in asm):
			print("Warning! Function \"" + self.name + "\" has no return!")
			
		return asm
