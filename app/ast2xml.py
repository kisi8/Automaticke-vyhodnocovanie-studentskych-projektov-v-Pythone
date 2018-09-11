#!/usr/bin/env python3
'''
From http://code.activestate.com/recipes/578625-python-ast-to-xml/
Ryan Gonzalez, MIT licensed

2015-02-05 Robert Stewart <rstewart@izeni.com> "Simplify output schema for further parsing."
'''


import ast, re, sys
from xml.dom import minidom

try:
    from xml.etree import cElementTree as etree
except:
    try:
        from lxml import etree
    except:
        from xml.etree import ElementTree as etree

def prettify(xml_string):
    reparsed = minidom.parseString(xml_string)
    return reparsed.toprettyxml(indent="  ")

class ast2xml(ast.NodeVisitor):
    def __init__(self):
        super(ast.NodeVisitor, self).__init__()
        self.path = []
        self.root = etree.Element('ast')
        self.celement = self.root
    def convert(self, tree):
        self.visit(tree)
        return etree.tostring(self.root, encoding='utf-8')
    def generic_visit(self, node):
        node_name = type(node).__name__
        self.path.append(node_name)
        ocelement = self.celement
        self.celement = etree.SubElement(self.celement, node_name)
        for item in node.__dict__:
            if isinstance(getattr(node, item), ast.AST):
                self.generic_visit(getattr(node, item))
            elif isinstance(getattr(node, item), list):
                ocel2 = self.celement
                self.celement = etree.SubElement(self.celement, item)
                [self.generic_visit(childnode) for childnode in getattr(node, item) if isinstance(childnode, (ast.AST, list))]
                self.celement = ocel2
            else:
                self.celement.attrib.update({item: str(getattr(node, item))})
        self.path.pop()
        self.celement = ocelement

def convert(filepath):
    with open(filepath, encoding='utf-8', mode ='r') as f:
        tree = ast.parse(f.read())
    res = ast2xml().convert(tree)
    res = res.replace(b"\x07", b"\\a")
    res = res.replace(b"\x08", b"\\b")
    res = res.replace(b"\x0c", b"\\f")
    res = res.replace(b"&#10;", b"\\n")
    res = res.replace(b"&#10;", b"\\r")
    res = res.replace(b"&#09;", b"\\t")
    res = res.replace(b"\x0b", b"\\v")
    return prettify(res)