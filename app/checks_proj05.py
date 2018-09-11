#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks_proj05.py

File containing all tests for 5th project.
'''

import constants
import ast2xml
from lxml import etree
from collections import OrderedDict
import imp

######### FUNCTIONS CHECK ########################

def functions_check(xml):
	'''
	Checking for usage of certain functions.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	function1 = tree.xpath('.//ClassDef[@name="Polynomial"]')
	function2 = tree.xpath('.//FunctionDef[@name="derivative"]')
	function3 = tree.xpath('.//FunctionDef[@name="at_value"]')
	if not function1 or not function2 or not function3:
		result.append('1')

	if result:
		result.insert(0, constants.FUNCTIONS5)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

######### DOCSTRING CHECK ########################

def docstrings(xml):
	'''
	Checking for usage of docstrings.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	functions = tree.xpath('.//FunctionDef')
	for j in range(len(functions)):
		lineno = tree.xpath('.//FunctionDef['+ str(j+1) +']/@lineno')
		doc = tree.xpath('.//FunctionDef['+ str(j+1) +']/body/Expr/Str')
		doc2 = tree.xpath('.//FunctionDef['+ str(j+1) +']/body/Expr/Str/@s')
		if not doc and lineno:
			result.append(lineno[0])
		if doc and doc2 == '' and lineno:
			result.append(lineno[0])

	functions = tree.xpath('.//ClassDef')
	for j in range(len(functions)):
		lineno = tree.xpath('.//ClassDef['+ str(j+1) +']/@lineno')
		doc = tree.xpath('.//ClassDef['+ str(j+1) +']/body/Expr/Str')
		doc2 = tree.xpath('.//ClassDef['+ str(j+1) +']/body/Expr/Str/@s')
		if not doc and lineno:
			result.append(lineno[0])
		if doc and doc2 == '' and lineno:
			result.append(lineno[0])

	if result:
		result.insert(0, constants.DOCSTRINGS)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

######### TYPE CHECK #############################

def type_check(xml):
	'''
	Checking for usage of type().

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	instance = tree.xpath('.//Call/Name')
	for i in range(len(instance)):
		ide = tree.xpath('(.//Call/Name)['+ str(i+1) +']/@id')
		if ide:
			if ide[0] == "type":
				lineno = tree.xpath('(.//Call/Name)['+ str(i+1) +']/@lineno')
				result.append(lineno[0])
	if result:
		result.insert(0, constants.TYPE)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

######### ASSERTS TESTS ##########################

def asserts_tests(filename):
	'''
	Function contains asserts for testing
	functionality of student's script.

	:param filename: name of the file
	:type filename: string

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	task1 = ''
	try:
		task1 = imp.load_source("proj05", constants.UPLOAD_FOLDER + "/%s" % filename)
	except:
		pass

	if task1:
		try:
			assert str(task1.Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
		except:
			result.append("assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == '3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
		except:
			result.append("assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == '3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
		except:
			result.append("assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == '3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x2=0)) == "0"
		except:
			result.append("assert str(Polynomial(x2=0)) == '0' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x0=0)) == "0"
		except:
			result.append("assert str(Polynomial(x0=0)) == '0' ." + constants.ASSERT_ERROR)

		try:
			assert task1.Polynomial(x0=2, x1=0, x3=0, x2=3) == task1.Polynomial(2,0,3)
		except:
			result.append("assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3) ." + constants.ASSERT_ERROR)

		try:
			assert task1.Polynomial(x2=0) == task1.Polynomial(x0=0)
		except:
			result.append("assert Polynomial(x2=0) == Polynomial(x0=0) ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x0=1)+task1.Polynomial(x1=1)) == "x + 1"
		except:
			result.append("assert str(Polynomial(x0=1)+Polynomial(x1=1)) == 'x + 1' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial([-1,1,1,0])+task1.Polynomial(1,-1,1)) == "2x^2"
		except:
			result.append("assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == '2x^2' ." + constants.ASSERT_ERROR)

		pol1 = task1.Polynomial(x2=3, x0=1)
		pol2 = task1.Polynomial(x1=1, x3=0)

		try:
			assert str(pol1+pol2) == "3x^2 + x + 1"
		except:
			result.append("pol1 = task1.Polynomial(x2=3, x0=1); pol2 = task1.Polynomial(x1=1, x3=0); assert str(pol1+pol2) == '3x^2 + x + 1' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x0=-1,x1=1)**1) == "x - 1"
		except:
			result.append("assert str(Polynomial(x0=-1,x1=1)**1) == 'x - 1' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x0=-1,x1=1)**2) == "x^2 - 2x + 1"
		except:
			result.append("assert str(Polynomial(x0=-1,x1=1)**2) == 'x^2 - 2x + 1' ." + constants.ASSERT_ERROR)

		pol3 = task1.Polynomial(x0=-1,x1=1)

		try:
			assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
		except:
			result.append("pol3 = task1.Polynomial(x0=-1,x1=1); assert str(pol3**4) == 'x^4 - 4x^3 + 6x^2 - 4x + 1' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x0=2).derivative()) == "0"
		except:
			result.append("assert str(Polynomial(x0=2).derivative()) == '0' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x3=2,x1=3,x0=2).derivative()) == "6x^2 + 3"
		except:
			result.append("assert str(Polynomial(x3=2,x1=3,x0=2).derivative()) == '6x^2 + 3' ." + constants.ASSERT_ERROR)

		try:
			assert str(task1.Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"
		except:
			result.append("assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == '12x' ." + constants.ASSERT_ERROR)

		pol4 = task1.Polynomial(x3=2,x1=3,x0=2)

		try:
			assert str(pol4.derivative()) == "6x^2 + 3"
		except:
			result.append("pol4 = task1.Polynomial(x3=2,x1=3,x0=2); assert str(pol4.derivative()) == '6x^2 + 3' ." + constants.ASSERT_ERROR)

		try:
			assert task1.Polynomial(-2,3,4,-5).at_value(0) == -2
		except:
			result.append("assert Polynomial(-2,3,4,-5).at_value(0) == -2 ." + constants.ASSERT_ERROR)

		try:
			assert task1.Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
		except:
			result.append("assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20 ." + constants.ASSERT_ERROR)

		try:
			assert task1.Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44
		except:
			result.append("assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44 ." + constants.ASSERT_ERROR)

		pol5 = task1.Polynomial([1,0,-2])

		try:
			assert pol5.at_value(-2.4) == -10.52
		except:
			result.append("pol5 = task1.Polynomial([1,0,-2]); assert pol5.at_value(-2.4) == -10.52 ." + constants.ASSERT_ERROR)

		try:
			assert pol5.at_value(-1,3.6) == -23.92
		except:
			result.append("pol5 = task1.Polynomial([1,0,-2]); assert pol5.at_value(-1,3.6) == -23.92 ." + constants.ASSERT_ERROR)

	return result

##################################################

#xml = ast2xml.convert('/Users/Juraj/Desktop/BP/file2.py')

#with open('/Users/Juraj/Desktop/BP/app/good.txt', 'w') as file:
#    file.write(xml)

#print(type_check(xml))