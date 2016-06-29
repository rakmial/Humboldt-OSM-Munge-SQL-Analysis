# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        discountcaps = element.attrib['k'].lower()
        if problemchars.search(discountcaps):
            keys['problemchars'] += 1
        elif lower_colon.search(discountcaps):
            keys['lower_colon'] += 1
        elif lower.search(discountcaps):
            keys['lower'] += 1
        else:
            keys['other'] += 1

    return keys

def other_keys(element):                #prints 'other' keys, discounts all-caps 'others'
    if element.tag == "tag":
        discountcaps = element.attrib['k'].lower()
        if not problemchars.search(discountcaps):
            if not lower_colon.search(discountcaps):
                if not lower.search(discountcaps):
                    return discountcaps


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    otherlist = []
    otherdict = {}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        otherlist.append(other_keys(element))
    for other in otherlist:
        if other in otherdict:
            otherdict[other] += 1
        else:
            otherdict[other] = 1

    return keys, otherdict

print process_map(r'C:\Users\Bash\Desktop\Udacity\2_Data_Analysis\P3\Project\sample.osm')
