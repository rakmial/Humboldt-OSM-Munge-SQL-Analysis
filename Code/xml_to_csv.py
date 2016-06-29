# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import csv
import codecs
import cerberus
import schema

''' variables used in process_map and subfunctions shape_element and validate_element'''
NODES_PATH = r"C:\Users\Bash\Desktop\Udacity\2_Data Analysis\P3\Project\CSVs\nodes.csv"
NODE_TAGS_PATH = r"C:\Users\Bash\Desktop\Udacity\2_Data Analysis\P3\Project\CSVs\nodes_tags.csv"
WAYS_PATH = r"C:\Users\Bash\Desktop\Udacity\2_Data Analysis\P3\Project\CSVs\ways.csv"
WAY_NODES_PATH = r"C:\Users\Bash\Desktop\Udacity\2_Data Analysis\P3\Project\CSVs\ways_nodes.csv"
WAY_TAGS_PATH = r"C:\Users\Bash\Desktop\Udacity\2_Data Analysis\P3\Project\CSVs\ways_tags.csv"

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']

WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
SCHEMA = schema.schema

'''used in process_map()'''
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):  #used in process_map()
    """Clean and shape node or way XML element to Python dict"""

    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    attr_list = [0000, 0.00, 0.00, "Missing Value", 0000, "Missing Value", 0000, "Missing Value"]

    for field in NODE_FIELDS:
        fieldindex = NODE_FIELDS.index(field)
        if field in element.attrib:
            attr_list[fieldindex] = element.attrib[field]

        node_attribs = dict(zip(NODE_FIELDS,attr_list))
        node_attribs['id'] = int(node_attribs['id'])
        node_attribs['lat'] = float(node_attribs['lat'])
        node_attribs['lon'] = float(node_attribs['lon'])
        node_attribs['uid'] = int(node_attribs['uid'])
        node_attribs['changeset'] = int(node_attribs['changeset'])
        node_attribs['user'] = unicode(node_attribs['user'])



    ndcounter = -1

    for child in element:
        if child.tag == 'tag':
            kval = ""
            tagtype = ""
            if re.search(PROBLEMCHARS,child.attrib['k']) != None:
                pass
            elif re.search(LOWER_COLON,child.attrib['k']) != None:
                colon_index = child.attrib['k'].find(':')
                tagtype = child.attrib['k'][:colon_index]
                kval = child.attrib['k'][colon_index+1:]
            else:
                kval = child.attrib['k']

            if tagtype == "":
                tagtype = default_tag_type

            tags.append({
                'id': element.attrib['id'],
                'key': kval,
                'value': child.attrib['v'],
                'type': tagtype
            })
        if child.tag == 'nd':
            ndcounter += 1
            way_nodes.append({
                'id': element.attrib['id'],
                'node_id': child.attrib['ref'],
                'position': ndcounter
            })

    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        way_attribs = dict(node_attribs)
        del way_attribs['lat'], way_attribs['lon']
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

def get_element(osm_file, tags=('node', 'way', 'relation')):    #used in process_map()
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def validate_element(element, validator, schema=SCHEMA):    #used in process_map()
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )

class UnicodeDictWriter(csv.DictWriter, object):      #used in process_map()
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def process_map(file_in, validate=True):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

process_map(r'C:\Users\Bash\Desktop\Udacity\2_Data Analysis\P3\Project\humboldt_california.osm\humboldt_california.osm')
