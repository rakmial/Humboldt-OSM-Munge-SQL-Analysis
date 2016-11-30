# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import sys
print (sys.version)
from pprint import pprint

mapping = { "St": "Street",
            "St.": "Street",
            "street": "Street",
            "Dr": "Drive",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "Int": "Intersection",
            "Blvd": "Boulevard",
            "Ln": "Lane",
            "Rnch": "Ranch",
            "Ctr": "Center"
            }

OSM_FILE = r"/run/media/jtl/Seagate Backup Plus Drive/Udacity/2_Data_Analysis/P3/Project/ProjectRepo/sample.osm"
OUTPUT_FILE = r"/run/media/jtl/Seagate Backup Plus Drive/Udacity/2_Data_Analysis/P3/Project/ProjectRepo/update_sample.osm"

def update_name(name, mapping):     # used in updater
    newname = None
    namesplit = name.split()
    for key, value in mapping.iteritems():
        if namesplit[-1] == key:
                newname = name.replace(key,value)
    if newname == None:
        return name
    return newname


def updater(osm_file):
    osmfile = open(osm_file,"r+")
    treeparse = ET.iterparse(osm_file, events=("start","end"))
    _, root = next(treeparse)
    for event, elem in treeparse:
        if event == 'end' and (elem.tag in ["node", "way"] ):
            maybename = ""
            istiger = False
            for tag in elem.iter("tag"):
                istiger = False
                if tag.attrib['k'] == "addr:street":
                    if tag.attrib['v'] != update_name(tag.attrib['v'], mapping):
                        print ('Before:', tag.attrib['v'])
                        tag.attrib['v'] = update_name(tag.attrib['v'], mapping)
                        print ('After:', tag.attrib['v'])
                if tag.attrib['k'] == 'name':
                    maybename = tag.attrib['v']
                if tag.attrib['k'] == "tiger:name_base":
                    istiger = True
                if istiger:
                    for tag in elem.iter("tag"):
                        if tag.attrib['k'] == "name":
                            if tag.attrib['v'] != update_name(tag.attrib['v'], mapping):
                                print ('Before:', tag.attrib['v'])
                                tag.attrib['v'] = update_name(tag.attrib['v'], mapping)
                                print ('After:', tag.attrib['v'])

        yield elem
        root.clear()
    osmfile.close()

with open(OUTPUT_FILE, 'w') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    for i, element in enumerate(updater(OSM_FILE)):
        print (ET.tostring(element, encoding='utf-8')[:10])
        output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')
