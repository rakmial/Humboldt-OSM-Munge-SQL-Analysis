# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problem_chars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        discount_caps = element.attrib['k'].lower()
        if problem_chars.search(discount_caps):
            keys['problem_chars'] += 1
        elif lower_colon.search(discount_caps):
            keys['lower_colon'] += 1
        elif lower.search(discount_caps):
            keys['lower'] += 1
        else:
            keys['other'] += 1

    return keys

def other_keys(element):                #prints 'other' keys, discounts all-caps 'others'
    if element.tag == "tag":
        discount_caps = element.attrib['k'].lower()
        if not problem_chars.search(discount_caps):
            if not lower_colon.search(discount_caps):
                if not lower.search(discount_caps):
                    return discount_caps


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problem_chars": 0, "other": 0}
    other_list = []
    other_dict = {}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        other_list.append(other_keys(element))
    for other in other_list:
        if other in other_dict:
            other_dict[other] += 1
        else:
            other_dict[other] = 1

    return keys, other_dict

print process_map(r'C:\Users\Bash\Desktop\Udacity\2_Data_Analysis\P3\Project\sample.osm')
