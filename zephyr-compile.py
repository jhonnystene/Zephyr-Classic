#!/usr/bin/env python3
import os, sys

import zephyr

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

sourceFile = zephyr.SourceFile(fileContents)
for function in sourceFile.functions:
	print("==== FUNCTION \"" + function + "\" CODE ====")
	print(sourceFile.functions[function].asm)
