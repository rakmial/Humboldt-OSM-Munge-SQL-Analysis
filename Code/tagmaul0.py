# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET


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
    treeparse = ET.iterparse(osm_file, events=("start",))
    for event, elem in treeparse:
        if elem.tag == "node" or elem.tag == "way":
            maybename = ""
            istiger = False
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:street":
                    if tag.attrib['v'] != update_name(tag.attrib['v'], mapping):
                        print 'Before:', tag.attrib['v']
                        tag.attrib['v'] = update_name(tag.attrib['v'], mapping)
                        print 'After:', tag.attrib['v']
                if tag.attrib['k'] == 'name':
                    maybename = tag.attrib['v']
                if tag.attrib['k'] == "tiger:name_base":
                    istiger = True
            if istiger:
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "name":
                        if tag.attrib['v'] != update_name(tag.attrib['v'], mapping):
                            print 'Before:', tag.attrib['v']
                            tag.attrib['v'] = update_name(tag.attrib['v'], mapping)
                            print 'After:', tag.attrib['v']

        #osmfile.write(ET.tostring(elem))
    osmfile.close()

#need to rehandle tiger name

updater(r'C:\Users\Bash\Desktop\Udacity\2_Data_Analysis\P3\Project\humboldt_california.osm\humboldt_california.osm')
