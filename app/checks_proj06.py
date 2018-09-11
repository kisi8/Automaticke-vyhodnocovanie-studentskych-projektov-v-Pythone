#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks_proj06.py

File containing all tests for 6th project.
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
	function1 = tree.xpath('.//FunctionDef[@name="first_nonrepeating"]')
	function2 = tree.xpath('.//FunctionDef[@name="combine4"]')
	if not function1 or not function2:
		result.append('1')

	if result:
		result.insert(0, constants.FUNCTIONS6)
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

############### NON ARG1 CHECK ###################

def non_args(xml):
	'''
	Checking for correct usage of arguments.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	instance = tree.xpath('.//FunctionDef[@name="first_nonrepeating"]/arguments/kw_defaults/following-sibling::arg')
	variable = tree.xpath('.//FunctionDef[@name="first_nonrepeating"]/arguments/arg')
	if instance or variable:
		lineno = tree.xpath('.//FunctionDef[@name="first_nonrepeating"]/@lineno')
		result.append(lineno[0])

	if result:
		result.insert(0, constants.LIMIT_ARGS)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

############### NON ARG2 CHECK ###################

def non_args_2(xml):
	'''
	Checking for correct usage of arguments.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	instance = tree.xpath('.//FunctionDef[@name="first_nonrepeating"]/arguments/args/*')
	if instance:
		if len(instance) > 1:
			lineno = tree.xpath('.//FunctionDef[@name="first_nonrepeating"]/@lineno')
			result.append(lineno[0])

	if result:
		result.insert(0, constants.NON_ARG_2)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

############### COMBINE ARG1 CHECK ###############

def combine_args(xml):
	'''
	Checking for correct usage of arguments.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	instance = tree.xpath('.//FunctionDef[@name="combine4"]/arguments/kw_defaults/following-sibling::arg')
	if instance:
		lineno = tree.xpath('.//FunctionDef[@name="combine4"]/@lineno')
		result.append(lineno[0])

	if result:
		result.insert(0, constants.LIMIT_ARGS)
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
		task1 = imp.load_source("proj06", constants.UPLOAD_FOLDER + "/%s" % filename)
	except:
		pass

	if task1:
		try:
			assert task1.first_nonrepeating('tooth') == 'h'
		except:
			result.append("assert first_nonrepeating('tooth') == 'h' ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('lool') == None
		except:
			result.append("assert first_nonrepeating('lool') == None ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('') == None
		except:
			result.append("assert first_nonrepeating('') == None ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('\t') == None
		except:
			result.append("assert first_nonrepeating('\\t') == None ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating(' ') == None
		except:
			result.append("assert first_nonrepeating(' ') == None ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('5') == '5'
		except:
			result.append("assert first_nonrepeating('5') == '5' ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('5655') == '6'
		except:
			result.append("assert first_nonrepeating('5655') == '6' ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('*/*') == '/'
		except:
			result.append("assert first_nonrepeating('*/*') == '/' ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('*/*/') == None
		except:
			result.append("assert first_nonrepeating('*/*/') == None ." + constants.ASSERT_ERROR)

		try:
			assert task1.first_nonrepeating('giusdgfdobhdafuignbuadfbioafhuabsfibasiffstzdgfasdfgcasdghftadgjszfjgzagdfabizbgfzdgsacf') == 'n'
		except:
			result.append("assert first_nonrepeating('giusdgfdobhdafuignbuadfbioafhuabsfibasiffstzdgfasdfgcasdghftadgjszfjgzagdfabizbgfzdgsacf') == 'n' ." + constants.ASSERT_ERROR)

		try:
			task1.first_nonrepeating(65)
		except:
			result.append("Funkcia by vám pri neočakávanom vstupe nemala padať: first_nonrepeating(65) .")

		try:
			task1.first_nonrepeating([6,5])
		except:
			result.append("Funkcia by vám pri neočakávanom vstupe nemala padať: first_nonrepeating([6,5]) .")

		try:
			task1.first_nonrepeating((6,5, 6))
		except:
			result.append("Funkcia by vám pri neočakávanom vstupe nemala padať: first_nonrepeating((6,5, 6)) .")

		try:
			task1.first_nonrepeating(('gdg', 'sad'))
		except:
			result.append("Funkcia by vám pri neočakávanom vstupe nemala padať: first_nonrepeating(('gdg', 'sad')) .")

		try:
			task1.first_nonrepeating({6,5, 6})
		except:
			result.append("Funkcia by vám pri neočakávanom vstupe nemala padať: first_nonrepeating({6,5, 6}) .")

		try:
			task1.first_nonrepeating({'name': 'john','code':6734})
		except:
			result.append("Funkcia by vám pri neočakávanom vstupe nemala padať: first_nonrepeating({'name': 'john','code':6734}) .")

		try:
		    vysledok = task1.combine4([6,6,5,2],36)

		    if len(vysledok) != len(set(vysledok)):
		        result.append('Výstup z combine4([6,6,5,2],36) by nemal obsahovať duplikáty.')

		    if len(vysledok) == 0:
		        result.append('Vo výstupe z combine4([6,6,5,2],36) sa musia objaviť nejaké výsledky.')

		    for expression in vysledok:
		        try:
		            if eval(expression) != 36:
		                result.append('Výstup ' + expression + ' z combine4([6,6,5,2],36) nevracia očakávaný výsledok 36.')
		        except:
		            result.append('Výstup ' + expression + ' nie je možné vyhodnotiť.')
		except:
		    result.append('Vo volaní combine4([6,6,5,2],36) nastala chyba, skontrolujte funkčnosť funkcie a jej návratový formát.')

		try:
		    vysledok = task1.combine4([6,6,5,2],-36)

		    if len(vysledok) != len(set(vysledok)):
		        result.append('Výstup z combine4([6,6,5,2],-36) by nemal obsahovať duplikáty.')

		    if len(vysledok) == 0:
		        result.append('Vo výstupe z combine4([6,6,5,2],-36) sa musia objaviť nejaké výsledky.')

		    for expression in vysledok:
		        try:
		            if eval(expression) != -36:
		                result.append('Výstup ' + expression + ' z combine4([6,6,5,2],-36) nevracia očakávaný výsledok -36.')
		        except:
		            result.append('Výstup ' + expression + ' nie je možné vyhodnotiť.')
		except:
		    result.append('Vo volaní combine4([6,6,5,2],-36) nastala chyba, skontrolujte funkčnosť funkcie a jej návratový formát.')

		try:
		    vysledok = task1.combine4([1,1,1,1],0)

		    if len(vysledok) != len(set(vysledok)):
		        result.append('Výstup z combine4([1,1,1,1],0) by nemal obsahovať duplikáty.')

		    if len(vysledok) < 5:
		        result.append('Vo výstupe z combine4([1,1,1,1],0) existuje aspoň 5 kombinácii.')

		    for expression in vysledok:
		        try:
		            if eval(expression) != 0:
		                result.append('Výstup ' + expression + ' z combine4([1,1,1,1],0) nevracia očakávaný výsledok 0.')
		        except:
		            result.append('Výstup ' + expression + ' nie je možné vyhodnotiť.')
		except:
		    result.append('Vo volaní combine4([1,1,1,1],0) nastala chyba, skontrolujte funkčnosť funkcie a jej návratový formát.')

		try:
		    vysledok = task1.combine4([6,6,5,2],17)

		    if len(vysledok) != len(set(vysledok)):
		        result.append('Výstup z combine4([6,6,5,2],17) by nemal obsahovať duplikáty.')

		    if len(vysledok) == 0:
		        result.append('Vo výstupe z combine4([6,6,5,2],17) sa musia objaviť nejaké výsledky.')

		    for expression in vysledok:
		        try:
		            if eval(expression) != 17:
		                result.append('Výstup ' + expression + ' z combine4([6,6,5,2],17) nevracia očakávaný výsledok 17.')
		        except:
		            result.append('Výstup ' + expression + ' nie je možné vyhodnotiť.')
		except:
		    result.append('Vo volaní combine4([6,6,5,2],17) nastala chyba, skontrolujte funkčnosť funkcie a jej návratový formát.')

		try:
		    vysledok = task1.combine4([6,6,5,2],-16)

		    if len(vysledok) != len(set(vysledok)):
		        result.append('Výstup z combine4([6,6,5,2],-16) by nemal obsahovať duplikáty.')

		    if len(vysledok) == 0:
		        result.append('Vo výstupe z combine4([6,6,5,2],-16) sa musia objaviť nejaké výsledky.')

		    for expression in vysledok:
		        try:
		            if eval(expression) != -16:
		                result.append('Výstup ' + expression + ' z combine4([6,6,5,2],-16) nevracia očakávaný výsledok -16.')
		        except:
		            result.append('Výstup ' + expression + ' nie je možné vyhodnotiť.')
		except:
		    result.append('Vo volaní combine4([6,6,5,2],-16) nastala chyba, skontrolujte funkčnosť funkcie a jej návratový formát.')

		try:
			assert task1.combine4([6,6,5,2],25) == []
		except:
			result.append("assert combine4([6,6,5,2],25) == [] ." + constants.ASSERT_ERROR)

		try:
			assert task1.combine4([6,6,5,2],-25) == []
		except:
			result.append("assert combine4([6,6,5,2],-25) == [] ." + constants.ASSERT_ERROR)

		try:
			assert task1.combine4([1,1,1,1],36) == []
		except:
			result.append("assert combine4([1,1,1,1],36) == [] ." + constants.ASSERT_ERROR)

		try:
			task1.combine4([6,6,5,2],'f')
			result.append("Funkcia by vám pri neočakávanom combine4([6,6,5,2],'f') mala vyhodiť výnimku alebo chybu.")
		except:
			pass

		try:
			task1.combine4([6,6,5,2],[36])
			result.append("Funkcia by vám pri neočakávanom combine4([6,6,5,2],[36]) mala vyhodiť výnimku alebo chybu.")
		except:
			pass

		try:
			task1.combine4([],[36])
			result.append("Funkcia by vám pri neočakávanom combine4([],[36]) mala vyhodiť výnimku alebo chybu.")
		except:
			pass

		try:
			task1.combine4([6],[36])
			result.append("Funkcia by vám pri neočakávanom combine4([6],[36]) mala vyhodiť výnimku alebo chybu.")
		except:
			pass

		try:
			task1.combine4([6,6],[36])
			result.append("Funkcia by vám pri neočakávanom combine4([6,6],[36]) mala vyhodiť výnimku alebo chybu.")
		except:
			pass

		try:
			task1.combine4([6,6,5],[36])
			result.append("Funkcia by vám pri neočakávanom combine4([6,6,5],[36]) mala vyhodiť výnimku alebo chybu.")
		except:
			pass

		try:
			task1.combine4([6,6,5,2,2],[36])
			result.append("Funkcia by vám pri neočakávanom combine4([6,6,5,2,2],[36]) mala vyhodiť výnimku alebo chybu.")
		except:
			pass

	return result

##################################################

#xml = ast2xml.convert('/Users/Juraj/Desktop/isj_proj06_xhanak34.py')

#with open('/Users/Juraj/Desktop/BP/app/good.txt', 'w') as file:
#    file.write(xml)

#print(combine_args(xml))