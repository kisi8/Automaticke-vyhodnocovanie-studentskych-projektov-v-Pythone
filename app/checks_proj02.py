#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks_proj02.py

File containing all tests for 2nd project.
'''

import constants
import ast2xml
from lxml import etree
from collections import OrderedDict
import helper
import os

######### GLOBAL LIST TEST ############################

def global_list(xml):
    '''
    Checking for correct lists in project template.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    listerin = tree.xpath('.//Module/body/Assign/List/elts/*')
    if len(listerin) != 8:
        lineno = tree.xpath('.//Module/body/Assign/List/@lineno')
        result.append(lineno[0])
    do = tree.xpath('.//Module/body/Assign/List/elts/Str[1]/@s')
    pre = tree.xpath('.//Module/body/Assign/List/elts/Str[2]/@s')
    du = tree.xpath('.//Module/body/Assign/List/elts/Str[3]/@s')
    du2 = tree.xpath('.//Module/body/Assign/List/elts/Str[4]/@s')
    do2 = tree.xpath('.//Module/body/Assign/List/elts/Str[5]/@s')
    za = tree.xpath('.//Module/body/Assign/List/elts/Str[6]/@s')
    du3 = tree.xpath('.//Module/body/Assign/List/elts/Str[7]/@s')
    du4 = tree.xpath('.//Module/body/Assign/List/elts/Str[8]/@s')
    if do[0] != 'do' or pre[0] != 'pre' or du[0] != 'du' or du2[0] != 'du' or do2[0] != 'do' or za[0] != 'za' or du3[0] != 'du' or du4[0] != 'du':
        lineno = tree.xpath('.//Module/body/Assign/List/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.GLOBAL_LIST)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### CORRECT OUTPUT TEST ##########################

def funguje_nefunguje(xml, filename):
    '''
    Checking for correct functioning
    of student's script.

    :param xml: xml structure
    :type xml: etree

    :param filename: name of the file
    :type filename: string

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    os.system('python /mnt/data/isj-2017-18/public/app/projects/%s > %s.txt' % (filename, filename))
    with open('/mnt/data/isj-2017-18/public/app/%s.txt' % filename) as file:
        out = file.readlines()
    if out:
        if out[0].find('nefunguje') != -1:
            lineno = tree.xpath('.//Module/body/If/Call/Name[@id="first_task"]/@lineno')
            result.append(lineno[0])
        if out[1].find('nefunguje') != -1:
            lineno = tree.xpath('.//Module/body/If/Call/Name[@id="second_task"]/@lineno')
            result.append(lineno[0])
        if out[2].find('nefunguje') != -1:
            lineno = tree.xpath('.//Module/body/If/Call/Name[@id="third_task"]/@lineno')
            result.append(lineno[0])
        if out[3].find('nefunguje') != -1:
            lineno = tree.xpath('.//Module/body/If/Call/Name[@id="fourth_task"]/@lineno')
            result.append(lineno[0])
        if out[4].find('nefunguje') != -1:
            lineno = tree.xpath('.//Module/body/If/Call/Name[@id="fifth_task"]/@lineno')
            result.append(lineno[0])

    if result:
        result.insert(0, constants.FUNGUJE_NEFUNGUJE)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FIRST TASK RETURN ############################

def first_task_return(xml):
    '''
    Checking for correct return value.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    ret = tree.xpath('.//FunctionDef[@name="first_task"]/body/Return/Compare/Name/@id')
    count = tree.xpath('.//FunctionDef[@name="first_task"]/body/Return/Compare/comparators/Num/@n')
    if not ret or not count:
        lineno = tree.xpath('.//FunctionDef[@name="first_task"]/body/Return/@lineno')
        result.append(lineno[0])
    elif ret[0] != 'vocabulary_size_eskymo' or count[0] != '4':
        lineno = tree.xpath('.//FunctionDef[@name="first_task"]/body/Return/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######## FIRST TASK SET ################################

def first_task_set(xml):
    '''
    Checking for usage of set().

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="first_task"]/body/Assign/Str/@s')
    if not nothing:
        sett = tree.xpath('.//FunctionDef[@name="first_task"]/body/Assign//Call/Name[@id="set"]')
        if not sett:
            lineno = tree.xpath('.//FunctionDef[@name="first_task"]/body//Assign//Name[@id="vocabulary_size_eskymo"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="first_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_SET)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######## FIRST TASK LENGHT #############################

def first_task_lenght(xml):
    '''
    Checking for usage of len().

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="first_task"]/body/Assign/Str/@s')
    if not nothing:
        lenght = tree.xpath('.//FunctionDef[@name="first_task"]/body/Assign//Call/Name[@id="len"]')
        if not lenght:
            lineno = tree.xpath('.//FunctionDef[@name="first_task"]/body//Assign//Name[@id="vocabulary_size_eskymo"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="first_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_LENGHT)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######## SECOND TASK LIST ##############################

def second_task_list(xml):
    '''
    Checking for correct lists in project template.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    prepos = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/List/elts/*')
    if len(prepos) != 3:
        lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/List/@lineno')
        result.append(lineno[0])
    str1 = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/List/elts/Str[1]/@s')
    str2 = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/List/elts/Str[2]/@s')
    str3 = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/List/elts/Str[3]/@s')
    if not str1 or not str2 or not str3:
        lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/List/@lineno')
        result.append(lineno[0])
    elif str1[0] != 'do' or str2[0] != 'za' or str3[0] != 'pred':
        lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign/List/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.SECOND_TASK_LIST)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######## SECOND TASK SET ################################

def second_task_set(xml):
    '''
    Checking for usage of set().

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign[2]/Str/@s')
    if not nothing:
        sett = tree.xpath('.//FunctionDef[@name="second_task"]/body//Assign//Call/Name[@id="set"]')
        if not sett:
            lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body//Assign//Name[@id="in_both_eskymo_prepos"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="second_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_SET)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######## SECOND TASK AND ################################

def second_task_and(xml):
    '''
    Checking for usage of and.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="second_task"]/body/Assign[2]/Str/@s')
    if not nothing:
        andd = tree.xpath('.//FunctionDef[@name="second_task"]/body//Assign//BitAnd')
        if not andd:
            lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body//Assign//Name[@id="in_both_eskymo_prepos"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="second_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.SECOND_TASK_AND)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### SECOND TASK RETURN ############################

def second_task_return(xml):
    '''
    Checking for correct return value.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    str1 = tree.xpath('.//FunctionDef[@name="second_task"]/body/Return/BoolOp/values/Compare[1]/comparators/Str/@s')
    str2 = tree.xpath('.//FunctionDef[@name="second_task"]/body/Return/BoolOp/values/Compare[2]/comparators/Str/@s')
    if not str1 or not str2:
        lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body/Return/@lineno')
        result.append(lineno[0])
    elif str1[0] != 'do;za' or str2[0] != 'za;do':
        lineno = tree.xpath('.//FunctionDef[@name="second_task"]/body/Return/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### THIRD TASK COLL ##############################

def third_task_coll(xml):
    '''
    Checking for usage of Counter().

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="third_task"]/body/Assign//Dict/keys')
    if not nothing:
        coll = tree.xpath('.//FunctionDef[@name="third_task"]/body//Assign//Call/Attribute[@attr="Counter"]/Name[@id="collections"]')
        if not coll:
            lineno = tree.xpath('.//FunctionDef[@name="third_task"]/body//Assign//Name[@id="wordfreq_eskymo"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="third_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.THIRD_TASK_COLL)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### THIRD TASK RETURN ############################

def third_task_return(xml):
    '''
    Checking for correct return value.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    str1 = tree.xpath('.//FunctionDef[@name="third_task"]/body/Return/Compare/comparators/Str/@s')
    if not str1:
        lineno = tree.xpath('.//FunctionDef[@name="third_task"]/body/Return/@lineno')
        result.append(lineno[0])
    elif str1[0] != 'do2pre1du4za1':
        lineno = tree.xpath('.//FunctionDef[@name="third_task"]/body/Return/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FOURTH TASK RETURN ###########################

def fourth_task_return(xml):
    '''
    Checking for correct return value.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    str1 = tree.xpath('.//FunctionDef[@name="fourth_task"]/body/Return/Compare/comparators/Str/@s')
    str2 = tree.xpath('.//FunctionDef[@name="fourth_task"]/body/Assign[1]/Str/@s')
    if not str1 or not str2:
        lineno = tree.xpath('.//FunctionDef[@name="fourth_task"]/@lineno')
        result.append(lineno[0])
    elif str1[0] != 'udub ut ubud u' or str2[0] != 'u dubu tu budu.':
        lineno = tree.xpath('.//FunctionDef[@name="fourth_task"]/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FOURTH TASK SLICE ############################

def fourth_task_slice(xml):
    '''
    Checking for usage of string slicing.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="fourth_task"]/body/Assign[2]/Str/@s')
    if not nothing:
        slicee = tree.xpath('.//FunctionDef[@name="fourth_task"]/body//Assign//Slice')
        if not slicee:
            lineno = tree.xpath('.//FunctionDef[@name="fourth_task"]/body/Assign[2]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="fourth_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.FOURTH_TASK_SLICE)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FIFTH TASK RETURN ############################

def fifth_task_return(xml):
    '''
    Checking for correct return value.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    str1 = tree.xpath('.//FunctionDef[@name="fifth_task"]/body/Return/Compare/comparators/Str/@s')
    str2 = tree.xpath('.//FunctionDef[@name="fifth_task"]/body/Assign[1]/Str/@s')
    if not str1 or not str2:
        lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/@lineno')
        result.append(lineno[0])
    elif str1[0] != 'Ut, re, mi, fa, sol, la, SI' or str2[0] != 'Hymn of St. John: Ut queant laxis re sonare fibris mi ra gestorum fa muli tuorum sol ve polluti la bii reatum SI Sancte Iohannes':
        lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/@lineno')
        result.append(lineno[0])

    if result:
        result.insert(0, constants.FIRST_TASK_RETURN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FIFTH TASK SPLIT #############################

def fifth_task_split(xml):
    '''
    Checking for usage of string slicing.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="fifth_task"]/body/Assign[2]/Str/@s')
    if not nothing:
        split = tree.xpath('.//FunctionDef[@name="fifth_task"]/body//Assign//Call/Attribute[@attr="split"]')
        if not split:
            lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/body//Assign//Name[@id="hymn_list"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.FIFTH_TASK_SPLIT)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FIFTH TASK SLICE #############################

def fifth_task_slice(xml):
    '''
    Checking for usage of string slicing.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="fifth_task"]/body/Assign[3]/Str/@s')
    if not nothing:
        slicee = tree.xpath('.//FunctionDef[@name="fifth_task"]/body//Assign//Slice')
        if not slicee:
            lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/body//Assign//Name[@id="skip2"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.FIFTH_TASK_SLICE)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

######### FIFTH TASK JOIN ##############################

def fifth_task_join(xml):
    '''
    Checking for usage of join().

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype
    '''
    result = []
    tree = etree.fromstring(xml)
    nothing = tree.xpath('.//FunctionDef[@name="fifth_task"]/body/Assign[4]/Str/@s')
    if not nothing:
        split = tree.xpath('.//FunctionDef[@name="fifth_task"]/body//Assign//Call/Attribute[@attr="join"]')
        if not split:
            lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/body//Assign//Name[@id="skip2_str"]/@lineno')
            if not lineno:
                lineno = tree.xpath('.//FunctionDef[@name="fifth_task"]/@lineno')
                result.append(lineno[0])
            else:
                result.append(lineno[0])

    if result:
        result.insert(0, constants.FIFTH_TASK_JOIN)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

########################################################

#xml = ast2xml.convert('/Users/Juraj/Desktop/BP/app/zadania/isj_proj02_xnovak00.py')
    
#with open('/Users/Juraj/Desktop/BP/app/good.txt', 'w') as file:
#    file.write(xml)
