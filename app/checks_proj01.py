#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks_proj01.py

File containing all tests for 1st project.
'''

import constants
import ast2xml
from lxml import etree
from collections import OrderedDict
import helper

######### FIRST TASK REGEX ############################

def first_task_string(xml):
    '''
    Checking for correct strings in project template.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    string = tree.xpath('.//FunctionDef[@name="test"]/body/Assert/Compare/Call/args/Str/@s')
    if string:
        if string[0] != 'bee(P: insect honey) dog  cat (P:milk) ant(P) ape':
            lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert/Compare/Call/args/Str/@lineno')
            result.append(lineno[0])

    if result:
        result.insert(0, constants.SECOND_TASK_STRING)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FIRST TASK REGEX ############################

def first_task_regex(xml):
    '''
    Checking for correct usage of regular expressions.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    regex = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/Call/args/Str/@s')
    if regex:
        nlookahead = regex[0].find('?!')
        lookbehind = regex[0].find('?<=')
        lookahead = regex[0].find('?=')
        if nlookahead == -1 or lookbehind == -1 or lookahead == -1:
            lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/Call/args/Str/@lineno')
            result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_REGEX)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### SECOND TASK REGEX ############################

def second_task_regex(xml):
    '''
    Checking for correct usage of regular expressions.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    regex = tree.xpath('.//FunctionDef[@name="first_task"]/body/Assign/Call/args/Str/@s')
    if regex:
        nlookahead = regex[0].find('?!')
        plookbehind = regex[0].find('?<=')
        if nlookahead == -1 or plookbehind == -1:
            lineno = tree.xpath('.//FunctionDef[@name="first_task"]/body/Assign/Call/args/Str/@lineno')
            result.append(lineno[0])

    if result:
        result.insert(0, constants.SECOND_TASK_REGEX)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######## SECOND TASK STRING ############################

def second_task_string(xml):
    '''
    Checking for correct strings in project template.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    string = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/Str/@s')
    string2 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Str/@s')
    if string and string2:
        if string[0] != 'Hello,John.I bought 192.168.0.1 for 100,000 bitcoins':
            lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/Str/@lineno')
            result.append(lineno[0])
        if string2[0] != 'Hello, John. I bought 192.168.0.1 for 100,000 bitcoins':
            lineno2 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Str/@lineno')
            result.append(lineno2[0])

    if result:
        result.insert(0, constants.SECOND_TASK_STRING)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################
