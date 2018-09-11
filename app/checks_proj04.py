#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks_proj04.py

File containing all tests for 4th project.
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
	function1 = tree.xpath('.//FunctionDef[@name="can_be_a_set_member_or_frozenset"]')
	function2 = tree.xpath('.//FunctionDef[@name="all_subsets"]')
	function3 = tree.xpath('.//FunctionDef[@name="all_subsets_excl_empty"]')
	if not function1 or not function2 or not function3:
		result.append('1')

	if result:
		result.insert(0, constants.FUNCTIONS)
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

	if result:
		result.insert(0, constants.DOCSTRINGS)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

######### IMPORT CHECK ###########################

def dont_import_task2(xml):
	'''
	Checking for not usage of import.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	imports = tree.xpath('.//Import/names/alias/@name')
	importsfrom = tree.xpath('.//ImportFrom/names/alias/@name')
	aliases = imports + importsfrom
	for alias in aliases:
		calls = tree.xpath('.//FunctionDef[@name="all_subsets"]/body//Call//Name/@id')
		for call in calls:
			if alias == call:
				lineno = tree.xpath('.//FunctionDef[@name="all_subsets"]/@lineno')
				result.append(lineno[0])

	if result:
		result.insert(0, constants.DONT_IMPORT)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

######### ISINSTANCE CHECK #######################

def isinstance_check(xml):
	'''
	Checking for usage of isinstance.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	instance = tree.xpath('.//FunctionDef[@name="can_be_a_set_member_or_frozenset"]/body//Call//Name[@id="isinstance"]')
	for i in range(len(instance)):
		lineno = tree.xpath('(.//FunctionDef[@name="can_be_a_set_member_or_frozenset"]/body//Call//Name[@id="isinstance"])['+ str(i+1) +']/@lineno')
		result.append(lineno[0])
	if result:
		result.insert(0, constants.ISINSTANCE)
	return list(reversed(OrderedDict.fromkeys(reversed(result))))

##################################################

######### LIMIT ARGS CHECK #######################

def limit_args_check(xml, filename):
	'''
	Checking for correct usage of arguemnts.

	:param xml: xml structure
	:type xml: etree

	:returns: list of recommendations
	:rtype: list
	'''
	result = []
	tree = etree.fromstring(xml)
	instance = tree.xpath('.//FunctionDef[@name="all_subsets_excl_empty"]/arguments/kw_defaults/following-sibling::arg')
	if instance:
		lineno = tree.xpath('.//FunctionDef[@name="all_subsets_excl_empty"]/@lineno')
		result.append(lineno[0])

	task3 = ''
	try:
		task3 = imp.load_source("proj04", constants.UPLOAD_FOLDER + "/%s" % filename)
	except:
		pass

	if task3:
		try: 
			assert task3.all_subsets_excl_empty(1, exclude_empty = False, unknown = 'nema byt') == [[], [1]]
		except:
			lineno = tree.xpath('.//FunctionDef[@name="all_subsets_excl_empty"]/@lineno')
			if lineno:
				result.append(lineno[0])

		try: 
			assert task1.all_subsets_excl_empty('a', 'b', 'c', unknown = 'nema byt', exclude_empty = True) == [['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
		except:
			lineno = tree.xpath('.//FunctionDef[@name="all_subsets_excl_empty"]/@lineno')
			if lineno:
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
		task1 = imp.load_source("proj04", constants.UPLOAD_FOLDER + "/%s" % filename)
	except:
		pass

	if task1:
		try:
			assert task1.can_be_a_set_member_or_frozenset(1) == 1
		except:
			result.append("assert can_be_a_set_member_or_frozenset(1) == 1 ." + constants.ASSERT_ERROR)
		try:
			assert task1.can_be_a_set_member_or_frozenset('1') == '1'
		except:
			result.append("assert can_be_a_set_member_or_frozenset('1') == '1' ." + constants.ASSERT_ERROR)
		try:
			assert task1.can_be_a_set_member_or_frozenset((1,2)) == (1,2)
		except:
			result.append("assert can_be_a_set_member_or_frozenset((1,2)) == (1,2) ." + constants.ASSERT_ERROR)
		try:
			assert task1.can_be_a_set_member_or_frozenset([1,2]) == frozenset([1,2])
		except:
			result.append("assert can_be_a_set_member_or_frozenset([1,2]) == frozenset([1,2]) ." + constants.ASSERT_ERROR)
		try:
			assert task1.can_be_a_set_member_or_frozenset({1,2}) == frozenset({1,2})
		except:
			result.append("assert .can_be_a_set_member_or_frozenset({1,2}) == frozenset({1,2}) ." + constants.ASSERT_ERROR)
		try:
			assert task1.can_be_a_set_member_or_frozenset({"d":5}) == frozenset({"d":5})
		except:
			result.append("assert can_be_a_set_member_or_frozenset({'d':5}) == frozenset({'d':5}) ." + constants.ASSERT_ERROR)
		try:
			assert task1.can_be_a_set_member_or_frozenset(set([1,2])) == frozenset([1,2])
		except:
			result.append("assert can_be_a_set_member_or_frozenset(set([1,2])) == frozenset([1,2]) ." + constants.ASSERT_ERROR)

		try:
			assert task1.all_subsets(['a', 'b', 'c']) == [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
		except:
			result.append("assert all_subsets(['a', 'b', 'c']) == [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets([]) == [[]]
		except:
			result.append("assert all_subsets([]) == [[]] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets(['a', 'b', 'c', 'ab']) == [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c'], ['ab'], ['a', 'ab'], ['b', 'ab'], ['a', 'b', 'ab'], ['c', 'ab'], ['a', 'c', 'ab'], ['b', 'c', 'ab'], ['a', 'b', 'c', 'ab']]
		except:
			result.append("assert all_subsets(['a', 'b', 'c', 'ab']) == [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c'], ['ab'], ['a', 'ab'], ['b', 'ab'], ['a', 'b', 'ab'], ['c', 'ab'], ['a', 'c', 'ab'], ['b', 'c', 'ab'], ['a', 'b', 'c', 'ab']] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets([5]) == [[], [5]]
		except:
			result.append("assert all_subsets([5]) == [[], [5]] ." + constants.ASSERT_ERROR)

		try:
			assert task1.all_subsets_excl_empty('a', 'b', 'c') == [['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
		except:
			result.append("all_subsets_excl_empty('a', 'b', 'c') == [['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets_excl_empty(1) == [[1]]
		except:
			result.append("assert all_subsets_excl_empty(1) == [[1]] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets_excl_empty(1, exclude_empty = True) == [[1]]
		except:
			result.append("assert all_subsets_excl_empty(1, exclude_empty = True) == [[1]] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets_excl_empty(1, exclude_empty = False) == [[], [1]]
		except:
			result.append("assert all_subsets_excl_empty(1, exclude_empty = False) == [[], [1]] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets_excl_empty('a', 'b', 'c', exclude_empty = True) == [['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
		except:
			result.append("assert all_subsets_excl_empty('a', 'b', 'c', exclude_empty = True) == [['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']] ." + constants.ASSERT_ERROR)
		try:
			assert task1.all_subsets_excl_empty('a', 'b', 'c', exclude_empty = False) == [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
		except:
			result.append("assert all_subsets_excl_empty('a', 'b', 'c', exclude_empty = False) == [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']] ." + constants.ASSERT_ERROR)

	return result

##################################################

#xml = ast2xml.convert('/Users/Juraj/Desktop/BP/file2.py')

#with open('/Users/Juraj/Desktop/BP/app/good.txt', 'w') as file:
#    file.write(xml)

#print(limit_args_check(xml, 'isj_proj04_xnovak00.py'))
