#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: checks.py

File containing all tests testing student's file.
'''

import py_compile
import sys
import os
import re
import glob
import pycodestyle
import constants
import ast2xml
from lxml import etree
from collections import OrderedDict
import helper
import checks_proj01
import checks_proj02
import checks_proj03
import checks_proj04
import checks_proj05
import checks_proj06
import checks_proj07

########## FILENAME AND LOGIN CHECK #################################

def filename_login(filename, login):
    '''
    Controling filename of student's script.

    :param filename: name of the file
    :type filename: string

    :param login: student's login
    :type login: string

    :returns: true/false
    :rtype: bool
    '''
    if len(filename) != 22:
        return False
    elif filename[:9] != 'isj_proj0':
        return False
    elif not filename[9].isdigit():
        return False
    elif filename[10:12] != '_x':
        return False
    elif not filename[17].isdigit():
        return False
    elif filename[19:] != '.py':
        return False
    elif filename[11:19] != login:
        return False
    else:
        return True

#####################################################################

########## PLAGIATISM CHECK #########################################

def plagiatism_check(filename):
    '''
    Controling plagiats of given file.

    :param filename: name of the file
    :type filename: string

    NOT IN USAGE
    '''
    compare = glob.glob(constants.UPLOAD_FOLDER + '/*.py')
    proj = filename[4:10]

    for item in compare:
        if str(item).find(proj) != -1:
            try:
                xml = ast2xml.convert('%s' % item)
                xml2 = ast2xml.convert(constants.UPLOAD_FOLDER + '/' + filename)
                tree = etree.fromstring(xml)
                tree2 = etree.fromstring(xml2)
                if helper.plagiatism(tree, tree2) and filename != item[-22:]:
                    with open('PLAGIAT-' + filename + '.txt', 'w') as file:
                        file.write(filename + '  ====>  ' + item[-22:])
            except:
                pass

#####################################################################

########## SHEBANG CHECK ############################################

def shebang_check(filepath):
    '''
    Controling correct shebang.

    :param filepath: path to the file
    :type filepath: string

    :returns: error message/none
    :rtype: list/string
    '''
    result = []
    she = False
    with open(filepath, 'r') as file:
        shebang = file.readline()
        for i in constants.SHEBANG:
            if(shebang.find(i, 0) != -1):
                she = True
        if not she:
            result.append(constants.SHEBANG_POPIS)
            result.append('1')
    return result

#####################################################################

########## PEP8 CHECK ###############################################

def pep8_check(filepath):
    '''
    Checking PEP 8 style.

    :param filepath: path to the file
    :type filepath: string

    :returns: PEP 8 report
    :rtype: string
    '''
    fchecker = pycodestyle.StyleGuide()
    return fchecker.input_file(filepath)

#####################################################################

########## SYNTAX CHECK ############################################

def syntax_check(filename):
    '''
    Checking syntax error of the file.

    :param filename: name of the file
    :type filename: string

    :returns: error message/none
    :rtype: string/int
    '''
    os.system('python /mnt/data/isj-2017-18/public/app/projects/%s 2> syntax.txt' % filename)
    with open('/mnt/data/isj-2017-18/public/app/syntax.txt') as file:
        content = file.read()

    ass = content.find('Error:')

    if ass != -1:
        return content
    return 0

#####################################################################

########## ASSERT CHECK #############################################

def assert_check(filename):
    '''
    Checking assertion errors.

    :param filename: name of the file
    :type filename: string

    :returns: error message/none
    :rtype: string/int
    '''
    os.system('python /mnt/data/isj-2017-18/public/app/projects/%s 2> assert.txt' % filename)
    with open('/mnt/data/isj-2017-18/public/app/assert.txt') as file:
        content = file.read()

    traceback = content.find('Traceback (most recent call last):')
    ass = content.find('AssertionError')

    if traceback != -1 and ass != -1:
        regex = re.compile(r'(?<=line\s)[0-9]+(?=,)', re.X)
        lineno = re.findall(regex, content)
        return lineno[-1]
    return 0

############ WITH OPEN ##############################################

def with_open(xml):
    '''
    Checking for correct usage of file openings.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    all_open = tree.xpath('.//Call/Name[@id="open"]/@lineno')
    good_open = tree.xpath('.//With/items/withitem/Call/Name[@id="open"]/@lineno')

    for line in all_open:
        if not(line in good_open):
            result.append(line)
    if result:
        result.insert(0, constants.WITH_OPEN)
    return result

#####################################################################

############ NESTED IF/ELIF #########################################

def nested_if(xml):
    '''
    Checking for nested if conditions.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    nested = tree.xpath('.//If/*[2]/If/*[2]/If/@lineno')

    for line in nested:
        result.append(line)
    if result:
        result.insert(0, constants.NESTED_IF)
    return result

#####################################################################

############ CHAIN COMPARISON #######################################
############ y < x < z ##############################################

def chain_comparison(xml):
    '''
    Checking for correct usage of chain comparison.
    y < x < z

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    compare = tree.xpath('.//Compare/@lineno')

    for j in range(len(compare)):
        indices = [i for i,x in enumerate(compare) if x == compare[j]]
        if len(indices) >= 2:
            for index in indices:
                ind = index + 1
                operand1 = tree.xpath('(.//Compare/comparators/Name/@id)['+ str(ind) +']')
                lineno1 = tree.xpath('(.//Compare/comparators/Name/@lineno)['+ str(ind) +']')
                operand3 = tree.xpath('(.//Compare/Name/@id)['+ str(ind) +']')
                lineno3 = tree.xpath('(.//Compare/Name/@lineno)['+ str(ind) +']')
                ind += 1
                operand2 = tree.xpath('(.//Compare/Name/@id)['+ str(ind) +']')
                lineno2 = tree.xpath('(.//Compare/Name/@lineno)['+ str(ind) +']')
                operand4 = tree.xpath('(.//Compare/comparators/Name/@id)['+ str(ind) +']')
                lineno4 = tree.xpath('(.//Compare/comparators/Name/@lineno)['+ str(ind) +']')
                if lineno1 and lineno2 and lineno3 and lineno4:
                    if ( ((operand1 and (operand1 == operand2)) or (operand3 and (operand3 == operand4))) and lineno1[0] == lineno2[0] == lineno3[0] == lineno4[0]):
                        result.append(compare[index])
    if result:
        result.insert(0, constants.CHAIN_COMPARISON)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

############### CHAIN COMPARISON IN IF/ELIF #########################
############### y == z == x == 'foo' ################################

def chain_comparison_if(xml):
    '''
    Checking for correct usage of chain comparison
    if if/else conditions.
    y == z == x == 'foo'

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    comparators = []
    tree = etree.fromstring(xml)
    ifs = tree.xpath('.//If')
    for j in range(len(ifs)):
        compares = tree.xpath('(.//If)['+ str(j+1) +']//Compare')
        for i in range(len(compares)):
            ops = tree.xpath('name(((.//If)['+ str(j+1) +']//Compare)['+ str(i+1) +']/ops/*)')
            if ops == 'Eq' or ops == 'NotEq':
                comparator = (tree.xpath('((.//If)['+ str(j+1) +']//Compare)['+ str(i+1) +']/comparators/*'))[0]
                comparators.append(comparator)

        for m in range(len(comparators)):
            for n in range(m + 1, len(comparators)):
                if helper.elements_equal(comparators[m], comparators[n]):
                    result.append(comparators[m].attrib['lineno'])

    if result:
        result.insert(0, constants.CHAIN_COMPARISON_IF)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

############ REPEATING VARIABLE IN IF/ELIF ##########################
############ y == r and y == a and y == g ###########################

def repeating_variable(xml):
    '''
    Checking for repeated variables in conditions.
    y == r and y == a and y == g

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    names = []
    names2 = []
    lineno = []
    tree = etree.fromstring(xml)
    ifs = tree.xpath('.//If')
    for j in range(len(ifs)):
        compares = tree.xpath('(.//If)['+ str(j+1) +']//Compare')
        for i in range(len(compares)):
            ops = tree.xpath('name(((.//If)['+ str(j+1) +']//Compare)['+ str(i+1) +']/ops/*)')
            if ops == 'Eq' or ops == 'NotEq':
                name = (tree.xpath('((.//If)['+ str(j+1) +']//Compare)['+ str(i+1) +']/*'))[0]
                lin = tree.xpath('((.//If)['+ str(j+1) +']//Compare)['+ str(i+1) +']/*/@lineno')
                if lin:
                    lineno.append(lin[0])
                names.append(name)
                name2 = (tree.xpath('((.//If)['+ str(j+1) +']//Compare)['+ str(i+1) +']/comparators/*'))[0]
                names2.append(name2)
        if len(set(lineno)) == 1:
            for m in range(len(names)):
                k = 0
                for n in range(m + 1, len(names)):
                    if helper.elements_equal(names[m], names[n]):
                        k += 1
                if k > 1:
                    result.append(names[m].attrib['lineno'])

            for m in range(len(names2)):
                k = 0
                for n in range(m + 1, len(names2)):
                    if helper.elements_equal(names2[m], names2[n]):
                        k += 1
                if k > 1:
                    result.append(names2[m].attrib['lineno'])

    if result:
        result.insert(0, constants.REPEATING_VARIABLE)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

############ COMPARE TO BOOL ########################################

def compare_to_bool(xml):
    '''
    Checking for incorrect comparings to bool.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    operators = ['Eq', 'NotEq', 'IsNot']
    values = ['True', 'False', 'None']
    tree = etree.fromstring(xml)
    ifs = tree.xpath('.//If')
    for i in range(len(ifs)):
        operator = tree.xpath('name(.//If['+ str(i+1) +']//Compare/ops/*)')
        if operator in operators:
            value = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/NameConstant/@value')
            if value and value[0] in values:
                result.append((tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/NameConstant/@lineno'))[0])
            else:
                elts = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/List/elts')
                tup = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/Tuple/elts')
                st = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/Set/elts')
                dic = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/Dict/keys')
                elts2 = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/List/elts/*')
                tup2 = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/Tuple/elts/*')
                st2 = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/Set/elts/*')
                dic2 = tree.xpath('.//If['+ str(i+1) +']//Compare/comparators/Dict/keys/*')
                if (elts and not elts2) or (tup and not tup2) or (st and not st2) or (dic and not dic2):
                    result.append((tree.xpath('.//If['+ str(i+1) +']//Compare/@lineno'))[0])
    if result:
        result.insert(0, constants.COMPARE_TO_BOOL)
    return result

#####################################################################

############ IN ITERABLE ############################################

def in_iterable(xml):
    '''
    Checking for not using in iterating tool.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    whil = tree.xpath('.//While')
    for i in range(len(whil)):
        lenght = tree.xpath('.//While['+ str(i+1) +']/Compare/comparators/Call/Name/@id')
        iterator = tree.xpath('.//While['+ str(i+1) +']/Compare/Name/@id')
        if lenght and iterator:
            if lenght[0] == 'len' and iterator[0]:

                augassign = tree.xpath('.//While['+ str(i+1) +']/body/AugAssign')
                for j in range(len(augassign)):
                    augname = tree.xpath('.//While['+ str(i+1) +']/body/AugAssign['+ str(j+1) +']/Name/@id')
                    store = tree.xpath('name(.//While['+ str(i+1) +']/body/AugAssign['+ str(j+1) +']/Name/*)')
                    if augname:
                        if augname[0] and augname[0] == iterator[0] and store == 'Store':
                            result.append((tree.xpath('.//While['+ str(i+1) +']/@lineno'))[0])

                assign = tree.xpath('.//While['+ str(i+1) +']/body/Assign')
                for j in range(len(assign)):
                    ass = tree.xpath('.//While['+ str(i+1) +']/body/Assign['+ str(j+1) +']/targets/Name/@id')
                    store = tree.xpath('name(.//While['+ str(i+1) +']/body/Assign['+ str(j+1) +']/targets/Name/*)')
                    if ass:
                        if ass[0] and ass[0] == iterator[0] and store == 'Store':
                            result.append((tree.xpath('.//While['+ str(i+1) +']/@lineno'))[0])

    if result:
        result.insert(0, constants.IN_ITERABLE)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

######## MUTABLE OBJECT AS DEAFULT VALUE IN FUNCTION ARGUMENT #######

def mutable_default_value(xml):
    '''
    Checking for empty mutable objects as 
    default value in function argument.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    funcs = tree.xpath('.//FunctionDef')
    for i in range(len(funcs)):
        defaults = tree.xpath('.//FunctionDef['+ str(i+1) +']/arguments/defaults/List')
        elts = tree.xpath('.//FunctionDef['+ str(i+1) +']/arguments/defaults/List/elts/*')
        if defaults and not elts:
            result.append((tree.xpath('.//FunctionDef['+ str(i+1) +']/@lineno'))[0])
        dic = tree.xpath('.//FunctionDef['+ str(i+1) +']/arguments/defaults/Dict')
        keys =  tree.xpath('.//FunctionDef['+ str(i+1) +']/arguments/defaults/Dict/keys/*')
        values =  tree.xpath('.//FunctionDef['+ str(i+1) +']/arguments/defaults/Dict/values/*')
        if dic and not keys and not values:
            result.append((tree.xpath('.//FunctionDef['+ str(i+1) +']/@lineno'))[0])

    if result:
        result.insert(0, constants.MUTABLE_DEFAULT_VALUE)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

############ RETURN EXPRESSION ######################################

def return_expression(xml):
    '''
    Checking for effective usage of return.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    returnes = tree.xpath('.//FunctionDef/body//Return')
    for i in range(len(returnes)):
        name = tree.xpath('(.//FunctionDef/body//Return)['+ str(i+1) +']/Name/@id')
        if name:
            store = tree.xpath('(name(.//FunctionDef/body//Assign//Name[@id="'+ name[0] +'"]/*))[last()]')
            if store and store == 'Store':
                result.append((tree.xpath('(.//FunctionDef/body//Return)['+ str(i+1) +']/Name[@id="'+ name[0] +'"]/@lineno'))[0])

    if result:
        result.insert(0, constants.RETURN_EXPRESSION)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

############ USE EXCEPTIONS TO THEIR FULLEST POTENTIAL ##############

def use_exceptions(xml):
    '''
    Checking for exceptions usage to their fullest potential.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    exceptions = tree.xpath('.//Try/handlers//ExceptHandler')
    for i in range(len(exceptions)):
        rais = tree.xpath('(.//Try/handlers//ExceptHandler)['+ str(i+1) +']/body//Raise')
        if not rais:
            result.append((tree.xpath('(.//Try/handlers//ExceptHandler)['+ str(i+1) +']/@lineno'))[0])

    if result:
        result.insert(0, constants.USE_EXCEPTIONS)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

############# CORE EXCEPTIONS #######################################

def core_exceptions(xml):
    '''
    Checking for dangerous exceptions usage.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    exceptions = ['RuntimeError', 'FloatingPointError', 'GeneratorExit', 'KeyboardInterrupt', 'MemoryError']
    tree = etree.fromstring(xml)
    rais = tree.xpath('.//Raise')
    for i in range(len(rais)):
        error = tree.xpath('.//Raise['+ str(i+1) +']/Call/Name/@id')
        if error and error[0] in exceptions:
            result.append((tree.xpath('.//Raise['+ str(i+1) +']/@lineno'))[0])

    if result:
        result.insert(0, constants.CORE_EXCEPTIONS)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

############# CHAIN ASSIGNMENT ######################################

def chain_assignment(xml):
    '''
    Checking for chain assignment.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    assigns = tree.xpath('.//Assign')
    for i in range(len(assigns)):
        name1 = tree.xpath('(.//Assign)['+ str(i+1) +']/targets/Name')
        name2 = tree.xpath('(.//Assign)['+ str(i+2) +']/targets/Name')
        if len(name1) == len(name2) == 1:
            store = tree.xpath('name((.//Assign)['+ str(i+1) +']/targets/Name/*)')
            if store == 'Store':
                assigner1 = tree.xpath('(.//Assign)['+ str(i+1) +']/*[2]')
                assigner2 = tree.xpath('(.//Assign)['+ str(i+2) +']/*[2]')
                lineno1 = tree.xpath('(.//Assign)['+ str(i+1) +']/*[2]/@lineno')
                lineno2 = tree.xpath('(.//Assign)['+ str(i+2) +']/*[2]/@lineno')
                str1 = tree.xpath('(.//Assign)['+ str(i+1) +']/Str/@s')
                str2 = tree.xpath('(.//Assign)['+ str(i+2) +']/Str/@s')
                if assigner1 and assigner2 and str1 and str2:
                    if str1[0] and str2[0]:
                        if helper.elements_equal(assigner1[0], assigner2[0]) and (int(lineno2[0]) - int(lineno1[0])) < 3:
                            result.append(lineno1[0])
                        
    if result:
        result.insert(0, constants.CHAIN_ASSIGNMENT)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

################## VARIABLES SWAP ###################################

def variables_swap(xml):
    '''
    Checking for C-like variable swap.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    assigns = tree.xpath('.//Assign')
    for i in range(len(assigns)):
        name1 = tree.xpath('(.//Assign)['+ str(i+1) +']/targets/Name/@id')
        name2 = tree.xpath('(.//Assign)['+ str(i+2) +']/targets/Name/@id')
        name3 = tree.xpath('(.//Assign)['+ str(i+3) +']/targets/Name/@id')
        if len(name1) == len(name2) == len(name3) == 1:
            store1 = tree.xpath('name((.//Assign)['+ str(i+1) +']/targets/Name/*)')
            store2 = tree.xpath('name((.//Assign)['+ str(i+2) +']/targets/Name/*)')
            store3 = tree.xpath('name((.//Assign)['+ str(i+3) +']/targets/Name/*)')
            if store1 == store2 == store3 == 'Store':
                loader1 = tree.xpath('(.//Assign)['+ str(i+1) +']/*[2]/@id')
                loader2 = tree.xpath('(.//Assign)['+ str(i+2) +']/*[2]/@id')
                loader3 = tree.xpath('(.//Assign)['+ str(i+3) +']/*[2]/@id')
                load1 = tree.xpath('name((.//Assign)['+ str(i+1) +']/*[2]/*)')
                load2 = tree.xpath('name((.//Assign)['+ str(i+2) +']/*[2]/*)')
                load3 = tree.xpath('name((.//Assign)['+ str(i+3) +']/*[2]/*)')
                if loader1 and loader2 and loader3 and load1 == load2 == load3 == 'Load':
                    if name1 == loader3 and name2 == loader1 and name3 == loader2:
                        lineno1 = tree.xpath('(.//Assign)['+ str(i+1) +']/targets/Name/@lineno')
                        lineno3 = tree.xpath('(.//Assign)['+ str(i+3) +']/targets/Name/@lineno')
                        if (int(lineno3[0]) - int(lineno1[0]) == 2):
                            result.append(lineno1[0])

    if result:
        result.insert(0, constants.VARIABLES_SWAP)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

################## REMOVE DUPLICATES FROM LIST #################################

def remove_duplicates_list(xml, filepath):
    '''
    Checking for incorrect removing duplicates from list.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    fors = tree.xpath('.//For')
    for i in range(len(fors)):
        iterator1 = tree.xpath('(.//For)['+ str(i+1) +']/Name[1]/@id')
        store1 = tree.xpath('name((.//For)['+ str(i+1) +']/Name/*)')
        if iterator1 and store1 == 'Store':
            load1 = tree.xpath('name((.//For)['+ str(i+1) +']/Name[2]/*)')
            if load1 == 'Load':
                list1 = tree.xpath('(.//For)['+ str(i+1) +']/Name[2]/@id')
                lineno1 = tree.xpath('(.//For)['+ str(i+1) +']/Name/@lineno')
                iterator2 = tree.xpath('(.//For)['+ str(i+1) +']/body/If[1]//Compare[1]/Name/@id')
                if list1 and lineno1 and iterator1 == iterator2:
                    list2 = tree.xpath('(.//For)['+ str(i+1) +']/body/If[1]//Compare[1]/comparators/Name/@id')
                    if list2:
                        append = tree.xpath('(.//For)['+ str(i+1) +']/body/If[1]//body//Expr/Call/Attribute/@attr')
                        if append:
                            if append[0] == 'append':
                                list3 = tree.xpath('(.//For)['+ str(i+1) +']/body/If[1]//body//Expr/Call/Attribute/Name/@id')
                                if list2 == list3:
                                    appender = tree.xpath('(.//For)['+ str(i+1) +']/body/If[1]//body//Expr/Call/args/Name/@id')
                                    lineno2 = tree.xpath('(.//For)['+ str(i+1) +']/body/If[1]//body//Expr/Call/args/Name/@lineno')
                                    if iterator1 == appender and lineno2:
                                        lineno3 = tree.xpath('//Name[preceding::For]/@lineno')
                                        if lineno3:
                                            helper.add_prints(filepath, lineno1[0], list1[0], lineno3[0], list2[0])
                                        helper.add_prints(filepath, lineno1[0], list1[0], lineno2[0], list2[0])
                                        os.system('python /mnt/data/isj-2017-18/public/app/prints.py > list.txt')
                                        with open('/mnt/data/isj-2017-18/public/app/list.txt') as file:
                                            out = file.readlines()
                                        if out:
                                            if out[0] == out[2] and list(set(list(out[1]))) == list(set(list(out[3]))):
                                                result.append((tree.xpath('(.//For)['+ str(i+1) +']/@lineno'))[0])

    if result:
        result.insert(0, constants.REMOVE_DUPLICATES_LIST)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))                                                              

#####################################################################

############## CHAIN STRING FUNCTIONS ###############################

def chain_string_functions(xml):
    '''
    Checking for correct usage of string functions.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    assigns = tree.xpath('.//Assign/*[2]')
    for i in range(len(assigns)):
        string = tree.xpath('name((.//Assign/*[2])['+ str(i+1) +'])')
        if string == 'Str':
            name1 = tree.xpath('(.//Assign)['+ str(i+1) +']/targets/Name/@id')
            if name1:
                lineno1 = tree.xpath('(.//Assign)['+ str(i+1) +']/targets/Name/@lineno')
                lineno2 = tree.xpath('.//Assign/Call/Attribute/Name[@id="%s"]/@lineno' % name1[0])
                if name1 and lineno1 and lineno2:
                    if (int(lineno2[0]) - int(lineno1[0])) == 2 or 1:
                        name2 = tree.xpath('.//Assign/targets/Name[@lineno="%s"]/@id' % lineno2[0])
                        if name2:
                            lineno3 = tree.xpath('.//Assign/Call/Attribute/Name[@id="%s"]/@lineno' % name2[0])
                            if lineno3:
                                name3 = tree.xpath('.//Assign/targets/Name[@lineno="%s"]/@id' % lineno3[0])
                                if name2 and lineno3 and name3:
                                    if (int(lineno3[0]) - int(lineno2[0])) == 2 or 1 and name2[0] == name3[0]:
                                        result.append(lineno3[0])
                
    if result:
        result.insert(0, constants.CHAIN_STRING_FUNCTIONS)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

################# CONCATENATE STRING IN LIST WITH JOIN ##############

def join_strings(xml):
    '''
    Checking for correct usage of .join
    when merginf strings.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    bom = 0
    tree = etree.fromstring(xml)
    fors = tree.xpath('.//For')
    for i in range(len(fors)):
        name = tree.xpath('(.//For)['+ str(i+1) +']/Name[2]/@id')
        lineno1 = tree.xpath('(.//For)['+ str(i+1) +']/Name[2]/@lineno')
        if name:
            store = tree.xpath('name(.//Assign/targets/Name[@id="%s"]/*)' % name[0])
            lineno2 = tree.xpath('.//Assign/targets/Name[@id="%s"]/@lineno' % name[0])
            lineno3 = tree.xpath('.//Assign/List/@lineno')
            if store and lineno2 and lineno3:
                for line in lineno3:
                    if store == 'Store' and lineno2[0] == line:
                        strings = tree.xpath('.//Assign/List/elts/*')
                        for j in range(len(strings)):
                            if str(strings[j]).find(' Str ') == -1:
                                bom = 1
                        if bom != 1:
                            store2 = tree.xpath('name((.//For)['+ str(i+1) +']/body//AugAssign/Name/*)')
                            aug = tree.xpath('name((.//For)['+ str(i+1) +']/body//AugAssign/*[2])')
                            if store2 and aug:
                                if store2 == 'Store' and aug == 'Add':
                                    result.append(lineno1[0])
                        bom = 0
    if result:
        result.insert(0, constants.JOIN_STRINGS)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

################ DO NOT USE MAP FUNCTION ############################

def dont_use_map(xml):
    '''
    Checking for incorrect usage of map.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    tree = etree.fromstring(xml)
    calls = tree.xpath('.//Call')
    for i in range(len(calls)):
        mp = tree.xpath('(.//Call)['+ str(i+1) +']/Name/@id')
        if mp:
            if mp[0] == 'map' or mp[0] == 'filter':
                result.append((tree.xpath('(.//Call)['+ str(i+1) +']/Name/@lineno'))[0])

    if result:
        result.insert(0, constants.DONT_USE_MAP)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

####################### USE SUM TO COUNT LIST ITEMS #################

def use_sum_list(xml):
    '''
    Checking for correct usage of sum
    when adding up numbers from list.

    :param xml: xml structure
    :type xml: etree

    :returns: list of recommendations
    :rtype: list
    '''
    result = []
    bom = 0
    tree = etree.fromstring(xml)
    fors = tree.xpath('.//For')
    for i in range(len(fors)):
        list1 = tree.xpath('(.//For)['+ str(i+1) +']/*[2]/@id')
        lineno1 = tree.xpath('(.//For)['+ str(i+1) +']/*[2]/@lineno')
        if list1 and lineno1:
            lineno2 = tree.xpath('.//Assign/targets/Name[@id="%s"]/@lineno' % list1[0])
            list2 = tree.xpath('name(.//Assign/*[2])')
            lineno3 = tree.xpath('.//Assign/*[2]/@lineno')
            if list2 and lineno2 and lineno3:
                if list2 == 'List' and lineno2[0] == lineno3[0] and int(lineno1[0]) > int(lineno3[0]):
                    nums = tree.xpath('.//Assign/*[2]/elts/*')
                    for j in range(len(nums)):
                        if str(nums[j]).find(' Num ') == -1:
                            bom = 1
                    if bom != 1:
                        store1 = tree.xpath('name((.//For)['+ str(i+1) +']/body//AugAssign/Name/*)')
                        aug = tree.xpath('name((.//For)['+ str(i+1) +']/body//AugAssign/*[2])')
                        if store1 and aug:
                            if store1 == 'Store' and aug == 'Add':
                                result.append(lineno1[0])
                    bom = 0

    if result:
        result.insert(0, constants.USE_SUM_LIST)
    return list(reversed(OrderedDict.fromkeys(reversed(result))))

#####################################################################

#xml = ast2xml.convert('/Users/Juraj/Desktop/BP/file.py')
    
#with open('/Users/Juraj/Desktop/BP/app/bad.txt', 'w') as file:
#    file.write(xml)

#print(repeating_variable(xml))

############ STMELENIE VŠETKÝCH VÝSLEDKOV TESTOV ####################

def checks(xml, filepath, filename):
    '''
    Merging all returns from functions.

    :param xml: xml structure
    :type xml: etree

    :param filepath: path to the file
    :type filepath: string

    :param filename: name of the file
    :type filename: string

    :returns: list of recommendations
    :rtype: list
'''
    result = []
    if filename.find('proj01') != -1:
        if assert_check(filename) != 0:
            result.append([constants.ASSERT, assert_check(filename)])
        result.append(checks_proj01.first_task_regex(xml))
        result.append(checks_proj01.first_task_string(xml))
        result.append(checks_proj01.second_task_regex(xml))
        result.append(checks_proj01.second_task_string(xml))
    if filename.find('proj02') != -1:
        result.append(checks_proj02.global_list(xml))
        result.append(checks_proj02.funguje_nefunguje(xml, filename))
        result.append(checks_proj02.first_task_return(xml))
        result.append(checks_proj02.first_task_set(xml))
        result.append(checks_proj02.first_task_lenght(xml))
        result.append(checks_proj02.second_task_list(xml))
        result.append(checks_proj02.second_task_set(xml))
        result.append(checks_proj02.second_task_and(xml))
        result.append(checks_proj02.second_task_return(xml))
        result.append(checks_proj02.third_task_coll(xml))
        result.append(checks_proj02.third_task_return(xml))
        result.append(checks_proj02.fourth_task_return(xml))
        result.append(checks_proj02.fourth_task_slice(xml))
        result.append(checks_proj02.fifth_task_return(xml))
        result.append(checks_proj02.fifth_task_split(xml))
        result.append(checks_proj02.fifth_task_slice(xml))
        result.append(checks_proj02.fifth_task_join(xml))
    if filename.find('proj03') != -1:
        if assert_check(filename) != 0:
            result.append([constants.ASSERT, assert_check(filename)])
        result.append(checks_proj03.match_permutations_sorted(xml))
        result.append(checks_proj03.match_permutations_assert(xml))
        result.append(checks_proj03.plur2sing_zip(xml))
        result.append(checks_proj03.plur2sing_return(xml))
        result.append(checks_proj03.vect2word_return(xml))
    if filename.find('proj04') != -1:
        for item in checks_proj04.asserts_tests(filename):
            result.append([item, '0'])
        result.append(checks_proj04.functions_check(xml))
        result.append(checks_proj04.docstrings(xml))
        result.append(checks_proj04.dont_import_task2(xml))
        result.append(checks_proj04.isinstance_check(xml))
        result.append(checks_proj04.limit_args_check(xml, filename))
    if filename.find('proj05') != -1:
        for item in checks_proj05.asserts_tests(filename):
            result.append([item, '0'])
        result.append(checks_proj05.functions_check(xml))
        result.append(checks_proj05.docstrings(xml))
        result.append(checks_proj05.type_check(xml))
    if filename.find('proj06') != -1:
        for item in checks_proj06.asserts_tests(filename):
            result.append([item, '0'])
        result.append(checks_proj06.functions_check(xml))
        result.append(checks_proj06.docstrings(xml))
        result.append(checks_proj06.non_args(xml))
        result.append(checks_proj06.non_args_2(xml))
        result.append(checks_proj06.combine_args(xml))
    if filename.find('proj07') != -1:
        for item in checks_proj07.asserts_tests(filename):
            result.append([item, '0'])
        result.append(checks_proj07.functions_check(xml))
        result.append(checks_proj07.docstrings(xml))
        result.append(checks_proj07.limit_calls_args(xml))
        result.append(checks_proj07.limit_calls_defaults(xml))
        result.append(checks_proj07.ordered_merge_args(xml))
    result.append(shebang_check(filepath))
    result.append(with_open(xml))
    result.append(nested_if(xml))
    result.append(chain_comparison(xml))
    result.append(repeating_variable(xml))
    result.append(compare_to_bool(xml))
    result.append(in_iterable(xml))
    result.append(mutable_default_value(xml))
    result.append(return_expression(xml))
    result.append(use_exceptions(xml))
    result.append(core_exceptions(xml))
    result.append(chain_assignment(xml))
    result.append(variables_swap(xml))
    result.append(remove_duplicates_list(xml, filepath))
    result.append(chain_string_functions(xml))
    result.append(join_strings(xml))
    #result.append(dont_use_map(xml))
    result.append(use_sum_list(xml))
    #plagiatism_check(filename)
    return result

#####################################################################
