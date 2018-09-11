#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks_proj07.py

File containing all tests for 7th project.
'''

import constants
import ast2xml
from lxml import etree
from collections import OrderedDict
import imp
import math
import os

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
	function1 = tree.xpath('.//FunctionDef[@name="limit_calls"]')
	function2 = tree.xpath('.//FunctionDef[@name="ordered_merge"]')
	function3 = tree.xpath('.//ClassDef[@name="Log"]//FunctionDef[@name="logging"]')
	if not function1 or not function2 or not function3:
		result.append('1')

	if result:
		result.insert(0, constants.FUNCTIONS7)
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
		if lineno:
			for li in lineno:
				doc = tree.xpath('.//FunctionDef[@lineno='+ li +']/body/Expr/Str')
				doc2 = tree.xpath('.//FunctionDef[@lineno='+ li +']/body/Expr/Str/@s')
				if not doc:		
					result.append(li)
				if doc and doc2 == '':
					result.append(li)

	functions = tree.xpath('.//ClassDef')
	for j in range(len(functions)):
		lineno = tree.xpath('.//ClassDef['+ str(j+1) +']/@lineno')
		if lineno:
			for li in lineno:
				doc = tree.xpath('.//ClassDef[@lineno='+ li +']/body/Expr/Str')
				doc2 = tree.xpath('.//ClassDef[@lineno='+ li +']/body/Expr/Str/@s')
				if not doc:		
					result.append(li)
				if doc and doc2 == '':
					result.append(li)

	if result:
		result.insert(0, constants.DOCSTRINGS)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

############ LIMIT CALLS ARGS ####################

def limit_calls_args(xml):
	'''
	Checking for correct usage of arguments.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	args = tree.xpath('.//FunctionDef[@name="limit_calls"]/arguments/args/*')
	if len(args) != 2:
		lineno = tree.xpath('.//FunctionDef[@name="limit_calls"]/@lineno')
		if lineno:
			result.append(lineno[0])
	else:
		arg1 = tree.xpath('.//FunctionDef[@name="limit_calls"]/arguments/args/arg[1]/@arg')
		arg2 = tree.xpath('.//FunctionDef[@name="limit_calls"]/arguments/args/arg[2]/@arg')
		if arg1 and arg2:
			if arg1[0] != "max_calls" or arg2[0] != "error_message_tail":
				lineno = tree.xpath('.//FunctionDef[@name="limit_calls"]/@lineno')
				if lineno:
					result.append(lineno[0])

	if result:
		result.insert(0, constants.LIMIT_CALLS_ARGS)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

############ LIMIT CALLS DEFAULTS ################

def limit_calls_defaults(xml):
	'''
	Checking for correct usage of arguments.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	args = tree.xpath('.//FunctionDef[@name="limit_calls"]/arguments/defaults/*')
	if len(args) != 2:
		lineno = tree.xpath('.//FunctionDef[@name="limit_calls"]/@lineno')
		if lineno:
			result.append(lineno[0])
	else:
		arg1 = tree.xpath('.//FunctionDef[@name="limit_calls"]/arguments/defaults/Num/@n')
		arg2 = tree.xpath('.//FunctionDef[@name="limit_calls"]/arguments/defaults/Str/@s')
		if arg1 and arg2:
			if int(arg1[0]) != 2 or arg2[0] != "called too often":
				lineno = tree.xpath('.//FunctionDef[@name="limit_calls"]/@lineno')
				if lineno:
					result.append(lineno[0])

	if result:
		result.insert(0, constants.LIMIT_CALLS_DEFAULTS)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

############ ORDERED MERGE ARGS ##################

def ordered_merge_args(xml):
	'''
	Checking for correct usage of arguments.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	found = False
	tree = etree.fromstring(xml)
	args = tree.xpath('.//FunctionDef[@name="ordered_merge"]/arguments//arg')
	if len(args) != 2:
		lineno = tree.xpath('.//FunctionDef[@name="ordered_merge"]/@lineno')
		if lineno:
			result.append(lineno[0])
	for j in range(len(args)):
		arg1 = tree.xpath('.//FunctionDef[@name="ordered_merge"]/arguments//arg['+ str(j+1) +']/@arg')
		for ar in arg1:
			if ar == "selector":
				found = True
	if not found:
		lineno = tree.xpath('.//FunctionDef[@name="limit_calls"]/@lineno')
		if lineno:
			result.append(lineno[0])

	if result:
		result.insert(0, constants.ORDERED_MERGE_ARGS)
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
		#task1 = imp.load_source("proj07", constants.UPLOAD_FOLDER + "/%s" % filename)
		task1 = imp.load_source("proj07", '/Users/Juraj/Desktop/BP/file2.py')
	except:
		pass

	if task1:
		try:
			try:
				@task1.limit_calls(1, 'that is too much')
				def pyth(a,b):
					c = math.sqrt(a**2 + b ** 2)
					return c
			except:
				result.append('Volanie dekorátora v tvare @limit_calls(1, "that is too much") zlyhalo. Overte jeho funkčnosť.')
			try:
				if pyth(3,4) != 5.0:
					result.append('limit_calls: Volanie pyth(3,4) pre math.sqrt(a**2 + b ** 2) nevracia správny výsledok.')
			except:
				result.append('limit_calls: Pri volaní pyth(3,4) pre math.sqrt(a**2 + b ** 2) nastala chyba.')

			try:
				pyth(6,8)
				result.append('Dekorátor @limit_calls(1, "that is too much") chybne povolil druhé volanie dekorovanej funkcie.')
			except:
				calls = str(sys.exc_info()[0]).find('TooManyCallsError')
				if calls == -1:
					result.append('Názov výnimky dekorátora limit_calls by podľa zadania mal byť TooManyCallsError.')
				err = str(sys.exc_info()[1]).find('function "pyth" - that is too much')
				if err == -1:
					result.append('Chybová správa by pre dekorovanú funkciu pyth() dekorátorom @limit_calls(1, "that is too much") mala vyzerať nasledovne: function "pyth" - that is too much')
		except:
			pass

		try:
			try:
				@task1.limit_calls(1)
				def pyth(a,b):
					c = math.sqrt(a**2 + b ** 2)
					return c
			except:
				result.append('Volanie dekorátora v tvare @limit_calls(1) zlyhalo. Overte jeho funkčnosť.')
			try:
				if pyth(3,4) != 5.0:
					result.append('limit_calls: Volanie pyth(3,4) pre math.sqrt(a**2 + b ** 2) nevracia správny výsledok.')
			except:
				result.append('limit_calls: Pri volaní pyth(3,4) pre math.sqrt(a**2 + b ** 2) nastala chyba.')

			try:
				pyth(6,8)
				result.append('Dekorátor @limit_calls(1, "that is too much") chybne povolil druhé volanie dekorovanej funkcie.')
			except:
				calls = str(sys.exc_info()[0]).find('TooManyCallsError')
				if calls == -1:
					result.append('Názov výnimky dekorátora limit_calls by podľa zadania mal byť TooManyCallsError.')
				err = str(sys.exc_info()[1]).find('function "pyth" - called too often')
				if err == -1:
					result.append('Chybová správa by pre dekorovanú funkciu pyth() dekorátorom @limit_calls(1) mala vyzerať nasledovne: function "pyth" - called too often')
		except:
			pass

		try:
			try:
				@task1.limit_calls(8)
				def pyth(a,b):
					c = math.sqrt(a**2 + b ** 2)
					return c
			except:
				result.append('Volanie dekorátora v tvare @limit_calls(8) zlyhalo. Overte jeho funkčnosť.')
			try:
				pyth(3,4)
				pyth(3,4)
				pyth(3,4)
				pyth(3,4)
				pyth(3,4)
				pyth(3,4)
				pyth(3,4)
				if pyth(3,4) != 5.0:
					result.append('limit_calls: Volanie pyth(3,4) pre math.sqrt(a**2 + b ** 2) nevracia správny výsledok.')
			except:
				result.append('limit_calls: Pri volaní pyth(3,4) pre math.sqrt(a**2 + b ** 2) nastala chyba.')

			try:
				pyth(3,4)
				result.append('Dekorátor @limit_calls(1, "that is too much") chybne povolil deviate volanie dekorovanej funkcie.')
			except:
				calls = str(sys.exc_info()[0]).find('TooManyCallsError')
				if calls == -1:
					result.append('Názov výnimky dekorátora limit_calls by podľa zadania mal byť TooManyCallsError.')
				err = str(sys.exc_info()[1]).find('function "pyth" - called too often')
				if err == -1:
					result.append('Chybová správa by pre dekorovanú funkciu pyth() dekorátorom @limit_calls(8) mala vyzerať nasledovne: function "pyth" - called too often')
		except:
			pass

		try:
			try:
				@task1.limit_calls()
				def pyth(a,b):
					c = math.sqrt(a**2 + b ** 2)
					return c
			except:
				result.append('Volanie dekorátora v tvare @limit_calls() zlyhalo. Overte jeho funkčnosť.')
			try:
				pyth(3,4)
				if pyth(3,4) != 5.0:
					result.append('limit_calls: Volanie pyth(3,4) pre math.sqrt(a**2 + b ** 2) nevracia správny výsledok.')
			except:
				result.append('limit_calls: Pri volaní pyth(3,4) pre math.sqrt(a**2 + b ** 2) nastala chyba.')

			try:
				pyth(3,4)
				result.append('Dekorátor limit_calls() chybne povolil tretie volanie dekorovanej funkcie.')
			except:
				calls = str(sys.exc_info()[0]).find('TooManyCallsError')
				if calls == -1:
					result.append('Názov výnimky dekorátora limit_calls by podľa zadania mal byť TooManyCallsError.')
				err = str(sys.exc_info()[1]).find('function "pyth" - called too often')
				if err == -1:
					result.append('Chybová správa by pre dekorovanú funkciu pyth() dekorátorom @limit_calls() mala vyzerať nasledovne: function "pyth" - called too often')
		except:
			pass

		try:
			try:
				@task1.limit_calls(error_message_tail='CHYBA')
				def pyth(a,b):
					c = math.sqrt(a**2 + b ** 2)
					return c
			except:
				result.append('Volanie dekorátora v tvare @limit_calls(error_message_tail="CHYBA") zlyhalo. Overte jeho funkčnosť.')
			try:
				pyth(3,4)
				if pyth(3,4) != 5.0:
					result.append('limit_calls: Volanie pyth(3,4) pre math.sqrt(a**2 + b ** 2) nevracia správny výsledok.')
			except:
				result.append('limit_calls: Pri volaní pyth(3,4) pre math.sqrt(a**2 + b ** 2) nastala chyba.')

			try:
				pyth(3,4)
				result.append('Dekorátor @limit_calls(error_message_tail="CHYBA") chybne povolil tretie volanie dekorovanej funkcie.')
			except:
				calls = str(sys.exc_info()[0]).find('TooManyCallsError')
				if calls == -1:
					result.append('Názov výnimky dekorátora limit_calls by podľa zadania mal byť TooManyCallsError.')
				err = str(sys.exc_info()[1]).find('function "pyth" - CHYBA')
				if err == -1:
					result.append('Chybová správa by pre dekorovanú funkciu pyth() dekorátorom @limit_calls(error_message_tail="CHYBA") mala vyzerať nasledovne: function "pyth" - CHYBA')
		except:
			pass

		try:
			try:
				@task1.limit_calls(max_calls=2, error_message_tail='CHYBA')
				def pyth(a,b):
					c = math.sqrt(a**2 + b ** 2)
					return c
			except:
				result.append('Volanie dekorátora v tvare @limit_calls(max_calls=2, error_message_tail="CHYBA") zlyhalo. Overte jeho funkčnosť.')
			try:
				pyth(3,4)
				if pyth(3,4) != 5.0:
					result.append('limit_calls: Volanie pyth(3,4) pre math.sqrt(a**2 + b ** 2) nevracia správny výsledok.')
			except:
				result.append('limit_calls: Pri volaní pyth(3,4) pre math.sqrt(a**2 + b ** 2) nastala chyba.')

			try:
				pyth(3,4)
				result.append('Dekorátor @limit_calls(max_calls=2, error_message_tail="CHYBA") chybne povolil tretie volanie dekorovanej funkcie.')
			except:
				calls = str(sys.exc_info()[0]).find('TooManyCallsError')
				if calls == -1:
					result.append('Názov výnimky dekorátora limit_calls by podľa zadania mal byť TooManyCallsError.')
				err = str(sys.exc_info()[1]).find('function "pyth" - CHYBA')
				if err == -1:
					result.append('Chybová správa by pre dekorovanú funkciu pyth() dekorátorom @limit_calls(max_calls=2, error_message_tail="CHYBA") mala vyzerať nasledovne: function "pyth" - CHYBA')
		except:
			pass

		try:
			try:
				@task1.limit_calls(error_message_tail='')
				def pyth(a,b):
					c = math.sqrt(a**2 + b ** 2)
					return c
			except:
				result.append('Volanie dekorátora v tvare @limit_calls(error_message_tail="") zlyhalo. Overte jeho funkčnosť.')
			try:
				pyth(3,4)
				if pyth(3,4) != 5.0:
					result.append('limit_calls: Volanie pyth(3,4) pre math.sqrt(a**2 + b ** 2) nevracia správny výsledok.')
			except:
				result.append('limit_calls: Pri volaní pyth(3,4) pre math.sqrt(a**2 + b ** 2) nastala chyba.')

			try:
				pyth(3,4)
				result.append('Dekorátor @limit_calls(error_message_tail="") chybne povolil tretie volanie dekorovanej funkcie.')
			except:
				calls = str(sys.exc_info()[0]).find('TooManyCallsError')
				if calls == -1:
					result.append('Názov výnimky dekorátora limit_calls by podľa zadania mal byť TooManyCallsError.')
				err = str(sys.exc_info()[1]).find('function "pyth" - ')
				if err == -1:
					result.append('Chybová správa by pre dekorovanú funkciu pyth() dekorátorom @limit_calls(error_message_tail="") mala vyzerať nasledovne: function "pyth" - ')
		except:
			pass

		try:
			assert list(task1.ordered_merge('abcde', [1, 2, 3], (3.0, 3.14, 3.141), range(11, 44, 11), selector = [2,3,0,1,3,1])) == [3.0, 11, 'a', 1, 22, 2]
		except:
			result.append('assert list(ordered_merge("abcde", [1, 2, 3], (3.0, 3.14, 3.141), range(11, 44, 11), selector = [2,3,0,1,3,1])) == [3.0, 11, "a", 1, 22, 2] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge('abcde', [1, 2, 3], selector = [1,0,0])) == [1, 'a', 'b']
		except:
			result.append('assert list(ordered_merge("abcde", [1, 2, 3], selector = [1,0,0])) == [1, "a", "b"] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge('abcde', [1, 2, 3], selector = [1,0])) == [1, 'a']
		except:
			result.append('assert list(ordered_merge("abcde", [1, 2, 3], selector = [1,0])) == [1, "a"] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge('abcde', [1, 2, 3], selector = [])) == []
		except:
			result.append('assert list(ordered_merge("abcde", [1, 2, 3], selector = [])) == [] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge('abcde', [1, 2, 3], selector = [1,0,0,0,0,0])) == [1, 'a', 'b', 'c', 'd', 'e']
		except:
			result.append('assert list(ordered_merge("abcde", [1, 2, 3], selector = [1,0,0,0,0,0])) == [1, "a", "b", "c", "d", "e"] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge('abcde', range(11, 44, 11), selector = [1,0,1,1])) == [11, 'a', 22, 33]
		except:
			result.append('assert list(ordered_merge("abcde", range(11, 44, 11), selector = [1,0,1,1])) == [11, "a", 22, 33] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge(' ', selector = [0])) == [' ']
		except:
			result.append('assert list(ordered_merge(" ", selector = [0])) == [" "] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge('    ', selector = [0,0,0])) == [' ', ' ', ' ']
		except:
			result.append('assert list(ordered_merge("    ", selector = [0,0,0])) == [" ", " ", " "] .' + constants.ASSERT_ERROR)

		try:
			assert list(task1.ordered_merge('    ', (2.8,3.3), selector = [0,0,1,0,1])) == [' ', ' ', 2.8, ' ', 3.3]
		except:
			result.append('assert list(ordered_merge("    ", (2.8,3.3), selector = [0,0,1,0,1])) == [" ", " ", 2.8, " ", 3.3] .' + constants.ASSERT_ERROR)

		try:
			list(task1.ordered_merge('abcde', range(11, 44, 11), selector = [1,0,1,1,1]))
			result.append('Volanie funkcie ako list(ordered_merge("abcde", range(11, 44, 11), selector = [1,0,1,1,1])) by malo vracať chybu.')
		except:
			pass

		try:
			list(task1.ordered_merge('abcde', selector = [5]))
			result.append('Volanie funkcie ako list(ordered_merge("abcde", selector = [5])) by malo vracať chybu.')
		except:
			pass

		try:
			list(task1.ordered_merge('', selector = [0]))
			result.append('Volanie funkcie ako list(ordered_merge("", selector = [0])) by malo vracať chybu.')
		except:
			pass

		try:
			list(task1.ordered_merge('abcde', [1, 2, 3], (3.0, 3.14, 3.141), range(11, 44, 11), selector = [2,3,0,1,3,4]))
			result.append('Volanie funkcie ako list(ordered_merge("abcde", [1, 2, 3], (3.0, 3.14, 3.141), range(11, 44, 11), selector = [2,3,0,1,3,4])) by malo vracať chybu.')
		except:
			pass

		try:
			with task1.Log(filename + '.txt') as logfile:
				logfile.logging('Test1')
				logfile.logging('Test2')
				a = 1/0
				logfile.logging('Test3')
		except:
			try:
				with open(filename + '.txt') as f:
					content = f.readlines()
			except:
				pass
			if content:
				if len(content) == 4:
					if content[0] != 'Begin\n' or content[1] != 'Test1\n' or content[2] != 'Test2\n' or content[3] != 'End\n':
						result.append('Formát výpisu z triedy Log v cieľovom súbore neodpovedá tomu zo zadania. Skontrolujte napríklad zakončenie riadkov.')
				else:
					result.append('Pri zavolaní: with Log("subor.txt") as logfile...logfile.logging("Test1")...logfile.logging("Test2")...a = 1/0...logfile.logging("Test3") by v súbore mali byť presne 4 záznamy(Begin,Test1,Test2,End).')

		try:
			with task1.Log(filename + '.txt') as logfile:
				logfile.logging('Test1')
		except:
			result.append('Pri zavolaní: with Log("subor.txt") as logfile...logfile.logging("Test1") by script nemal padať.')
		try:
			with open(filename + '.txt') as f:
				content = f.readlines()
		except:
			pass
		if content:
			if len(content) == 3:
				if content[0] != 'Begin\n' or content[1] != 'Test1\n' or content[2] != 'End\n':
					result.append('Formát výpisu z triedy Log v cieľovom súbore neodpovedá tomu zo zadania. Skontrolujte napríklad zakončenie riadkov.')
			else:
				result.append('Pri zavolaní: with Log("subor.txt") as logfile...logfile.logging("Test1") by v súbore mali byť presne 3 záznamy(Begin,Test1,End).')

		try:
			with task1.Log(filename + '.txt') as logfile:
				a = 1/0
		except:
			try:
				with open(filename + '.txt') as f:
					content = f.readlines()
			except:
				pass
			if content:
				if len(content) == 2:
					if content[0] != 'Begin\n' or content[1] != 'End\n':
						result.append('Formát výpisu z triedy Log v cieľovom súbore neodpovedá tomu zo zadania. Skontrolujte napríklad zakončenie riadkov.')
				else:
					result.append('Pri zavolaní: with Log("subor.txt") as logfile...a = 1/0 by v súbore mali byť presne 2 záznamy(Begin,End).')

		try:
			os.remove(filename + '.txt')
		except:
			pass

	return result

##################################################

#xml = ast2xml.convert('/Users/Juraj/Desktop/BP/file2.py')

#with open('/Users/Juraj/Desktop/BP/app/good.txt', 'w') as file:
#    file.write(xml)

#print(asserts_tests('isj_proj07_xkysel12.py'))