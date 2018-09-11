#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks_proj03.py

File containing all tests for 3rd project.
'''

import constants
import ast2xml
from lxml import etree
from collections import OrderedDict
import helper
import os
import glob

######### MATCH PERMUTATIONS SORTED ####################

def match_permutations_sorted(xml):
    '''
    Checking for usage of sorted.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="match_permutations"]/body/Assign[2]/Str/@s')
    if not nothing:
        sort = tree.xpath('.//FunctionDef[@name="match_permutations"]/body//Assign//Call/Name[@id="sorted"]')
        if not sort:
            lineno = tree.xpath('.//FunctionDef[@name="match_permutations"]/body//Assign//Name[@id="matching_perms"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="match_permutations"]/@lineno')
                if lineno:
                    result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.MATCH_PERMUTATIONS_SORTED)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### MATCH PERMUTATIONS ASSERT ####################

def match_permutations_assert(xml):
    '''
    Checking for correct assertions in project template.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    str1 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/Compare/Call/args/Str[1]/@s')
    str2 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/Compare/Call/args/Set/elts/Str[1]/@s')
    str3 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/Compare/Call/args/Set/elts/Str[2]/@s')
    str4 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/Compare/Call/args/Set/elts/Str[3]/@s')
    str5 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/Compare/Call/args/Set/elts/Str[4]/@s')
    str6 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/Compare/comparators/List/elts/Str[1]/@s')
    str7 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/Compare/comparators/List/elts/Str[2]/@s')

    if not str1 or not str2 or not str3 or not str4 or not str5 or not str6 or not str7:
        lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/@lineno')
        if lineno:
            result.append(lineno[0])
    elif str1[0] != 'act' or str2[0] != 'cat' or str3[0] != 'rat' or str4[0] != 'dog' or str5[0] != 'act' or str6[0] != 'act' or str7[0] != 'cat':
        lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[1]/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### PLUR2SING ZIP ################################

def plur2sing_zip(xml):
    '''
    Checking for usage of zip().

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="plur2sing"]/body/Assign[2]/Str/@s')
    if not nothing:
        lineno = tree.xpath('.//FunctionDef[@name="plur2sing"]/body//Assign/targets/Name[@id="pl2sg"]/@lineno')
        if lineno:
            zipp = tree.xpath('.//FunctionDef[@name="plur2sing"]/body//Assign//Call/Name[@id="zip"][@lineno="%s"]' % lineno[0])
            if not zipp:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.PLUR2SING_ZIP)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### PLUR2SING RETURN #############################

def plur2sing_return(xml):
    '''
    Checking for correct return value.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    str1 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/List[1]/elts/Str[1]/@s')
    str2 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/List[1]/elts/Str[2]/@s')
    str3 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/List[1]/elts/Str[3]/@s')
    str4 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/List[2]/elts/Str[1]/@s')
    str5 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/List[2]/elts/Str[2]/@s')
    str6 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/Call/args/List[2]/elts/Str[3]/@s')
    str7 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Dict/keys/Str[1]/@s')
    str8 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Dict/keys/Str[2]/@s')
    str9 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Dict/keys/Str[3]/@s')
    str10 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Dict/values/Str[1]/@s')
    str11 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Dict/values/Str[2]/@s')
    str12 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/Compare/comparators/Dict/values/Str[3]/@s')

    if not str1 or not str2 or not str3 or not str4 or not str5 or not str6 or not str7 or not str8 or not str9 or \
       not str10 or not str11 or not str12:
        lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/@lineno')
        if lineno:
            result.append(lineno[0])
    elif str1[0] != 'goose' or str2[0] != 'man' or str3[0] != 'child' or str4[0] != 'geese' or str5[0] != 'men' or str6[0] != 'children' or \
         str7[0] != 'geese' or str8[0] != 'men' or str9[0] != 'children' or str10[0] != 'goose' or str11[0] != 'man' or str12[0] != 'child':
        lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[2]/@lineno')
        if lineno:
            result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### VECT2WORD RETURN #############################

def vect2word_return(xml):
    '''
    Checking for correct return value.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    str1 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/keys/Str[1]/@s')
    str2 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/keys/Str[2]/@s')
    str3 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/keys/Str[3]/@s')
    str4 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/keys/Str[4]/@s')
    str5 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[1]/elts/Num[1]/@n')
    str6 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[1]/elts/Num[2]/@n')
    str7 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[2]/elts/Num[1]/@n')
    str8 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[2]/elts/Num[2]/@n')
    str9 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[3]/elts/Num[1]/@n')
    str10 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[3]/elts/Num[2]/@n')
    str11 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[4]/elts/Num[1]/@n')
    str12 = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/Compare/Call/args/GeneratorExp/generators/comprehension/Call/args/Dict/values/List[4]/elts/Num[2]/@n')

    if not str1 or not str2 or not str3 or not str4 or not str5 or not str6 or not str7 or not str8 or not str9 or \
       not str10 or not str11 or not str12:
        lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/@lineno')
        if lineno:
            result.append(lineno[0])
    elif str1[0] != 'king' or str2[0] != 'queen' or str3[0] != 'uncle' or str4[0] != 'aunt' or str5[0] != '3' or str6[0] != '1' or \
         str7[0] != '6' or str8[0] != '3' or str9[0] != '4' or str10[0] != '3' or str11[0] != '8' or str12[0] != '9':
        lineno = tree.xpath('.//FunctionDef[@name="test"]/body/Assert[3]/@lineno')
        if lineno:
            result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

#xml = ast2xml.convert('/Users/Juraj/Desktop/BP/file2.py')
#tree = etree.fromstring(xml)

#with open('/Users/Juraj/Desktop/BP/app/good.txt', 'w') as file:
#    file.write(xml)
