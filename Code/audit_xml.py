# -*- coding: utf-8 -*-
import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Access", "Acres", "Airport", "Alley", "Bridge", "Camp", "Center",
            "Circle", "Cove", "Creek", "Crossing", "Gulch", "Heights", "Highway", "Hill", "Hollow","Loop",
            "Mainline","Park", "Pass", "Point", "Railroad", "Ranch", "Route", "Row", "Run", "Spring", "Terrace",
            "View", "Vista", "Way"]

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
            "Ctr": "Center",
            "lane": "Lane"
            }

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) #used in audit_street_type()

def audit_street_type(street_types, street_name): #used in audit()
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):   #used in audit()
    if (elem.attrib['k'] == "addr:street"):
        return True
    else:
        return False


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            maybename = ""
            istiger = False
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "name":
                    maybename = tag.attrib['v']
                if tag.attrib['k'] == "tiger:name_base":
                    istiger = True
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
            if istiger:
                audit_street_type(street_types,maybename)
    osm_file.close()
    pprint.pprint(dict(street_types))
    return street_types


audit(r'C:\Users\Bash\Desktop\Udacity\2_Data Analysis\P3\Project\humboldt_california.osm\humboldt_california.osm')
