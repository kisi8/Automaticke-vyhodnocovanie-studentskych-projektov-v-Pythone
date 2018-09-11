#!/usr/bin/env python3

'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: helper.py

File containing custom functions for helping
other functions.
'''

import os
import re

def source_code(filepath):
    '''
    Get source code from student file.

    :param filepath: path to the file
    :type filepath: string

    :returns: source code
    :rtype: string
'''
    with open(filepath, encoding='utf-8', mode='r') as file:
        code = file.read()
    return code

def pep8_make_html(filename):
    '''
    Making html file for PEP 8 report.

    :param filename: name of the file
    :type filename: string
    '''
    try:
        os.remove('/mnt/data/isj-2017-18/public/app/templates/%s-pep.html' % filename)
    except:
        pass
    os.system("pepper8 -o /mnt/data/isj-2017-18/public/app/templates/%s-pep.html pep.txt" % filename)
    with open('/mnt/data/isj-2017-18/public/app/templates/%s-pep.html' % filename, 'r') as file:
        lines = file.readlines()
        lines[5] = '<link href="/static/style.css" rel="stylesheet">'
        del lines[6:151]
    os.remove('/mnt/data/isj-2017-18/public/app/templates/%s-pep.html' % filename)
    with open('/mnt/data/isj-2017-18/public/app/templates/%s-pep.html' % filename, 'w') as file:
        file.writelines(lines)

def count_odporucania(list):
    '''
    Couting number of recommendations.

    :param list: list of functions reports
    :type filename: list

    :returns: number of recommendations
    :rtype: int
    '''
    result = 0
    for item in list:
        if item:
            result += 1
    return result

def add_prints(filepath, lineno1, list1, lineno2, list2):
    '''
    Helper function for remove_duplicates_list.

    :param filepath: path to the file
    :type filepath: string

    :param lineno1: line of the first list
    :type lineno1: string

    :param list1: first list
    :type list1: list

    :param lineno2: line of the second list
    :type lineno2: string

    :param list2: second list
    :type list2: list
    '''
    i = 0
    with open(filepath, encoding='utf-8', mode='r') as input_file, open('/mnt/data/isj-2017-18/public/app/prints.py', 'w') as output_file:
        lines = input_file.readlines()
        for line in lines:
            line = re.sub('print(.*)', '#', line)
            output_file.write(line)
        output_file.seek(0)
    with open('prints.py', 'r+') as output_file:
        lines = output_file.readlines()
        output_file.seek(0)
        lines.insert(int(lineno1)-1, 'print(%s)\n' % list1)
        lines.insert(int(lineno1)-1, 'print(type(%s))\n' % list1)
        lines.insert(int(lineno2)+2, 'print(%s)\n' % list2)
        lines.insert(int(lineno2)+2, '\nprint(type(%s))\n' % list2)
        output_file.writelines(lines)

def elements_equal(e1, e2):
    '''
    Determining if two elements are equal.

    :param e1: first element
    :type e1: element

    :param e2: second element
    :type e2: element

    :returns: true/false
    :rtype: bool
    '''
    if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    for key, item in e1.attrib.items():
        if key != 'lineno' and key != 'col_offset' and e2.attrib[key]:
            if e1.attrib[key] != e2.attrib[key]:
                return False
    if len(e1) != len(e2): return False

    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

def is_List_Empty(inList):
    '''
    Determining if given list is empty.

    :param inList: list
    :type inList: list

    :returns: true/false
    :rtype: bool
    '''
    if isinstance(inList, list):    # Is a list
        return all( map(is_List_Empty, inList) )
    return False # Not a list

def plagiatism(e1, e2):
    '''
    Function for comparing if two trees are similar.

    :param e1: first element
    :type e1: element

    :param e2: second element
    :type e2: element

    :returns: true/false
    :rtype: bool
    '''
    if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    for key, item in e1.attrib.items():
        if key != 'lineno' and key != 'col_offset' and key!= 'id' and e2.attrib[key]:
            if e1.attrib[key] != e2.attrib[key]:
                return False
    if len(e1) != len(e2): return False

    return all(plagiatism(c1, c2) for c1, c2 in zip(e1, e2))