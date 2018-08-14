from lxml import etree

def convertxmltodict(xml_root):
    new_dict = {}
    for child in xml_root:
        tag = child.tag.split('}', 1)[1]
        if tag not in new_dict:
            new_dict[tag] = {}
        ref = None
        if tag == 'applicationVisibilities':
            ref = child.find('application', xml_root.nsmap).text
        elif tag == 'classAccesses':
            ref = child.find('apexClass', xml_root.nsmap).text
        elif tag == 'custom' or tag == 'description' or tag == 'fullName':
            new_dict[tag] = child.text
        elif tag == 'customPermissions':
            ref = child.find('name', xml_root.nsmap).text
        elif tag == 'externalDataSourceAccesses':
            ref = child.find('name', xml_root.nsmap).text
        elif tag == 'fieldPermissions':
            ref = child.find('field', xml_root.nsmap).text
        elif tag == 'layoutAssignments':
            elem = child.find('recordType', xml_root.nsmap)
            if elem == None:
                elem = child.find('layout', xml_root.nsmap)
            if elem.tag.endswith('recordType'):
                ref = 'RT-'+elem.text
            else:
                ref = 'L-'+elem.text.split('-',maxsplit=1)[0]
        elif tag == 'loginHours':
            ref = 'all'
        elif tag == 'loginIpRanges':
            start = None
            end = None
            for item in child:
                itemtag = item.tag.split('}', 1)[1]
                if itemtag == 'startAddress':
                    start = item.text
                elif itemtag == 'endAddress':
                    end = item.text
            if start != None and end != None:
                ref = start + end
        elif tag == 'objectPermissions':
            ref = child.find('object', xml_root.nsmap).text
        elif tag == 'pageAccesses':
            ref = child.find('apexPage', xml_root.nsmap).text
        elif tag == 'profileActionOverrides':
            pass #TODO
        elif tag == 'recordTypeVisibilities':
            ref = child.find('recordType', xml_root.nsmap).text
        elif tag == 'tabVisibilities':
            ref = child.find('tab', xml_root.nsmap).text
        elif tag == 'userLicense':
            new_dict[tag] = child.text
        elif tag == 'userPermissions':
            ref = child.find('name', xml_root.nsmap).text
        else:
            print('WARNING: ' + tag + ' is not a supported profile permission')

        if ref != None:
            value = {}
            for item in child:
                itemtag = item.tag.split('}', 1)[1]
                value[itemtag] = item.text
            new_dict[tag][ref] = value
    return new_dict

def mergeprofiles(from_profile,to_profile):
    
    for key in from_profile.keys():
        if key == 'custom' or key == 'fullName' or key == 'userLicense':
            continue
        if key == 'description' or key == 'loginHours':
            to_profile[key] = from_profile[key]
        if key in to_profile:
            for subkey in from_profile[key].keys():
                to_profile[key][subkey] = from_profile[key][subkey]
        else:
            to_profile[key] = from_profile[key]

    return to_profile


def convertdicttoxml(in_dict):
    root = etree.Element('{http://soap.sforce.com/2006/04/metadata}Profile', nsmap={None: 'http://soap.sforce.com/2006/04/metadata'})
    keys = sorted(in_dict.keys())
    for key in keys:   
        value = in_dict[key]  
        if key == 'custom' or key == 'description' or key == 'fullName' or key == 'userLicense':
            elem = etree.SubElement(root, key)
            elem.text = value
        elif key == 'profileActionOverrides':
            pass  # TODO
        elif key == 'loginHours':
            elem = etree.SubElement(root,key)
            for attr, val in value['all'].items():
                subelem = etree.SubElement(elem, attr)
                subelem.text = val
        else:
            sub_keys = sorted(value.keys())
            for sub_key in sub_keys:
                item = value[sub_key]
                elem = etree.SubElement(root,key)
                for attr, val in item.items():
                    subelem = etree.SubElement(elem,attr)
                    subelem.text = val
    return root


def mergetheseprofiles(from_profile_filename, to_profile_filename, export_to):
    tree_to = etree.parse(to_profile_filename)
    root_to = tree_to.getroot()
    tree_from = etree.parse(from_profile_filename)
    root_from = tree_from.getroot()
    from_dict = convertxmltodict(root_from)
    to_dict = convertxmltodict(root_to)
    merged = mergeprofiles(from_profile=from_dict, to_profile=to_dict)

    final_xml = convertdicttoxml(merged)

    final_file = etree.tostring(
        final_xml, encoding='utf-8', xml_declaration=True, pretty_print=True)
    file = open(export_to, 'w')
    file.write(final_file.decode('utf-8').replace('  ', '    '))
    file.close()
