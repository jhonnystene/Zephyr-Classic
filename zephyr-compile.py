#!/usr/bin/env python3
# Exit codes:
# 0 - Success
# 1 - Invalid arguments
# 2 - Couldn't open file
# 3 - Syntax error
# 4 - Missing #mainfunc
# 5 - Trying to use reserved name
# 6 - Preprocessor directive in function

import os, sys

from zephyr import SourceFile

try:
	fileName = sys.argv[1]
except:
	print("Usage: zephyr-compile <zephyr source file> <optional: output filename>")
	sys.exit(1)

try:
	outFileName = sys.argv[2]
except:
	print("WARN: No output file.")
	outFileName = False

try:
	fileContents = open(fileName).read()
except:
	print("Error! Couldn't open " + fileName)
	sys.exit(2)

sourceFile = SourceFile.createFrom(fileContents)
if(outFileName):
	pass
	with open(outFileName, "w") as outfile:
		outfile.write(sourceFile.genASM())
	print("Compile success!")
else:
	print("Generated source code: ")
	print("")
	print(sourceFile.genASM())
sys.exit(0)
