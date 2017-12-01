"""
..class:: CAOMxml
    :synopsis: The CAOMxml class allows for more reliable transport of multiple
    variables associated with a CAOM XML entry by reducing the number of
    complex dictionary operations and indexing assumptions needed in
    hlsp_to_xml.py and its children.
"""

from lxml import etree

#--------------------

class CAOMxml:

    def __init__(self, label):
        """
        Create a new CAOMxml object with a few default parameters.
        """
        #Common properties
        self.label = label
        self.parent = "CompositeObservation"
        self.source = None

    def send_to_lxml(self, xmltree):
        """
        Create a new subelement within xmltree for a given CAOMxml object.
        Multiple parameters read from the CAOMxml object are used to organize,
        label, and otherwise fill out the XML entry.
        """
        #Search every element of the xmltree.
        for element in xmltree.iter():

            #Create a new subelement if an element matches the CAOMxml object's
            #'parent' parameter.
            if element.tag == self.parent:
                print("Found parent for {1}: {0}".format(self.parent, self.label))
                entry = etree.SubElement(element, self.label)
                if self.source == "VALUE":
                    s = etree.SubElement(entry, "source")
                    s.text = self.source
                    v = etree.SubElement(entry, "value")
                    v.text = self.value
                elif self.source == "HEADER":
                    s = etree.SubElement(entry, "source")
                    s.text = self.source
                    hn = etree.SubElement(entry, "headerName")
                    hn.text = self.headerName
                    hk = etree.SubElement(entry, "headerKeyword")
                    hk.text = self.headerKeyword
                    hdv = etree.SubElement(entry, "headerDefaultValue")
                    hdv.text = self.headerDefaultValue
                elif self.label == "product":
                    cl = etree.SubElement(entry, "calibrationLevel")
                    cl.text = self.calibrationLevel
                    ct = etree.SubElement(entry, "contentType")
                    ct.text = self.contentType
                    dpt = etree.SubElement(entry, "dataProductType")
                    dpt.text = self.dataProductType
                    fnd = etree.SubElement(entry, "fileNameDescriptor")
                    fnd.text = self.fileNameDescriptor
                    fs = etree.SubElement(entry, "fileStatus")
                    fs.text = self.fileStatus
                    ft = etree.SubElement(entry, "fileType")
                    ft.text = self.fileType
                    pn = etree.SubElement(entry, "planeNumber")
                    pn.text = self.planeNumber
                    pt = etree.SubElement(entry, "productType")
                    pt.text = self.productType
                    rt = etree.SubElement(entry, "releaseType")
                    rt.text = self.releaseType
                    sa = etree.SubElement(entry, "statusAction")
                    sa.text = self.statusAction
                return xmltree

        #If the 'parent' parameter is not found in xmltree, create it as a new
        #subelement and try again.
        new_parent = etree.SubElement(xmltree.getroot(), self.parent)
        return self.send_to_lxml(xmltree)

    def __str__(self):
        return "{0}: parent={1}".format(self.label,
                                        self.parent)

#--------------------

class CAOMvalue(CAOMxml):

    def __init__(self, label):
        CAOMxml.__init__(self, label)
        self.source = "VALUE"
        self.value = "None"

    def __str__(self):
        return "{0}: parent={1}, value={2}".format(self.label,
                                                   self.parent,
                                                   self.value)

#--------------------

class CAOMheader(CAOMxml):

    def __init__(self, label):
        CAOMxml.__init__(self, label)
        self.source = "HEADER"
        self.headerName = "PRIMARY"
        self.headerKeyword = None
        self.headerDefaultValue = "None"

    def __str__(self):
        return ("{0}: parent={1}, headerName={2}, headerKeyword={3}"
                .format(self.label,
                        self.parent,
                        self.headerName,
                        self.headerKeyword))

#--------------------

class CAOMproduct(CAOMxml):

    def __init__(self):
        CAOMxml.__init__(self, label="product")
        self.parent = "productList"
        self.calibrationLevel = "HLSP"
        self.contentType = None
        self.dataProductType = None
        self.fileNameDescriptor = "FILEROOT"
        self.fileStatus = None
        self.fileType = None
        self.planeNumber = "1"
        self.productType = None
        self.releaseType = "DATA"
        self.statusAction = None

    def __str__(self):
        return ("{0}: contentType={1}, fileType={2}, productType={3}"
                .format(self.label,
                        self.contentType,
                        self.fileType,
                        self.productType))

#--------------------

class CAOMxmlList:

    def __init__(self):
        self.members = []
        self.labels = []

    def add(self, caom_obj):
        if not isinstance(caom_obj, CAOMxml):
            print("CAOMxmlList cannot accept members other than CAOMxml!")
            return self
        self.members.append(caom_obj)
        self.labels.append(caom_obj.label)

    def findlabel(self, target):
        assert isinstance(target, str)
        if target in self.labels:
            for m in self.members:
                if m.label == target:
                    return m
        else:
            return None

    def findheader(self, target):
        assert isinstance(target, str)
        for m in self.members:
            if isinstance(m, CAOMheader):
                if m.headerKeyword == target:
                    return m
        else:
            return None

#--------------------

if __name__ == "__main__":
    x = CAOMproduct()
    print(x.label)
    print(x.parent)
    x.properties()
