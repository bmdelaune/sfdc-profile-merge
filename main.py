from lxml import etree
import json
import sfdc_profile_merge as profile

tree_to = etree.parse('in/full.profile')
root_to = tree_to.getroot()

tree_from = etree.parse('in/small.profile')
root_from = tree_from.getroot()

from_dict = profile.convertxmltodict(root_from)
to_dict = profile.convertxmltodict(root_to)

merged = profile.mergeprofiles(from_profile=from_dict,to_profile=to_dict)

final_xml = profile.convertdicttoxml(merged)

print(etree.tostring(final_xml))
