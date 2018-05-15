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
        elif tag == 'custom':
            new_dict[tag] = child.text
        elif tag == 'fieldPermissions':
            ref = child.find('field', xml_root.nsmap).text
        elif tag == 'layoutAssignments':
            elem = child.find('recordType', xml_root.nsmap)
            if elem == None:
                elem = child.find('layout', xml_root.nsmap)
            if elem.tag.endswith('recordType'):
                ref = 'RT-'+elem.text
            else:
                ref = 'L-'+elem.text
        elif tag == 'loginIpRanges':
            if type(new_dict[tag]) is dict:
                new_dict[tag] = []
            value = {}
            for item in child:
                itemtag = item.tag.split('}', 1)[1]
                value[itemtag] = item.text
            new_dict[tag].append(value)
        elif tag == 'objectPermissions':
            ref = child.find('object', xml_root.nsmap).text
        elif tag == 'pageAccesses':
            ref = child.find('apexPage', xml_root.nsmap).text
        elif tag == 'recordTypeVisibilities':
            ref = child.find('recordType', xml_root.nsmap).text
        elif tag == 'tabVisibilities':
            ref = child.find('tab', xml_root.nsmap).text
        elif tag == 'userLicense':
            new_dict[tag] = child.text
        elif tag == 'userPermissions':
            ref = child.find('name', xml_root.nsmap).text
        else:
            print(tag)

        if ref != None:
            value = {}
            for item in child:
                itemtag = item.tag.split('}', 1)[1]
                value[itemtag] = item.text
            new_dict[tag][ref] = value
    return new_dict

def mergeprofiles(from_profile,to_profile):
    return {**from_profile, **to_profile}

def convertdicttoxml(in_dict):
    root = etree.Element('Profile')
    keys = sorted(in_dict.keys())
    for key in keys:   
        value = in_dict[key]  
        if key == 'custom':
            elem = etree.SubElement(root, key)
            elem.text = value
        elif key == 'layoutAssignments':
            pass
        elif key == 'loginIpRanges':
            for item in value:
                elem = etree.SubElement(root, key)
                for attr, val in item.items():
                    subelem = etree.SubElement(elem, attr)
                    subelem.text = val
        elif key == 'userLicense':
            elem = etree.SubElement(root, key)
            elem.text = value
        else:
            sub_keys = sorted(value.keys())
            for sub_key in sub_keys:
                item = value[sub_key]
                elem = etree.SubElement(root,key)
                for attr, val in item.items():
                    subelem = etree.SubElement(elem,attr)
                    subelem.text = val
    return root


