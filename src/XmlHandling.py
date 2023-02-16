import xml.etree.ElementTree as ET
# <SSHJail><Host ip="Host1" freedate="01.01.2023" /><Host ip="Host2" freedate="02.02.2023" /><Host ip="Host3" freedate="03.03.2023" /></SSHJail>

def DictToXml(dictionary: dict, path: str) -> None:
    # create the root element
    root = ET.Element('SSHJail')

    # create a sub-element for each key-value pair in the dictionary
    for host, date in dictionary.items():
        subelement = ET.SubElement(root, 'Host')
        subelement.set('ip', host)
        subelement.set('freedate', date)

    # create an ElementTree object with the root element
    tree = ET.ElementTree(root)

    # write the ElementTree object to an XML file
    tree.write(path)

# DictToXml(SSHJail, 'SSHJail.xml')

def RemoveFromXml(path: str, subelement_name: str, attribute_name: str, value: str) -> None:
    # parse the XML file and get the root element
    tree = ET.parse(path)
    root = tree.getroot()

    # find the subelement to remove
    for subelement in root.findall(subelement_name):
        if subelement.get(attribute_name) == value:
            root.remove(subelement)

    # write the modified tree to the same file
    tree.write(path)

# RemoveFromXml('SSHJail.xml', 'Host', 'ip', 'Host1')