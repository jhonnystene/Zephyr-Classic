#!/usr/bin/env python3
# Exit codes:
# 0 - Success
# 1 - Invalid arguments
# 2 - Couldn't open file
# 3 - Syntax error
# 4 - Missing #mainfunc
# 5 - Trying to use reserved name

import os, sys

from zephyr import SourceFile

try:
	fileName = sys.argv[1]
except:
	print("Usage: zephyr-compile <zephyr source file>")
	sys.exit(1)

try:
	fileContents = open(fileName).read()
except:
	print("Error! Couldn't open " + fileName)
	sys.exit(2)

sourceFile = SourceFile.createFrom(fileContents)
print("Generated source code: ")
print("")
print(sourceFile.genASM())
sys.exit(0)
