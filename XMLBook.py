from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree

xmlFD = -1
bookDoc = None

def LoadXMLFromFile():
    global xmlFD, bookDoc
    fileName = str(input("Please input file name to load! : "))

    try:
        xmlFD = open(fileName)
    except IOError:
        print("Invaild file path...")
    else:
        try:
            dom = parse(xmlFD)
        except Exception:
            print("Parse error...")
        else:
            print("XML Document loading complete")
            bookDoc = dom
            return dom
    return None

class XMLBook:
    def __init__(self):
        self.document = None
        pass

    def LoadFromFile(self):
        fileName = str(input("Please input file name to load! : "))

        try:
            xmlFD = open(fileName)
        except IOError:
            print("Invaild file path...")
        else:
            try:
                dom = parse(xmlFD)
            except Exception:
                print("Parse error...")
            else:
                print("XML Document loading complete")
                bookDoc = dom
                return dom
        return None

    def ReleaseDocument(self):
        if self.checkDocument():
            self.document.unlink()

    def PrintToXML(self):
        if self.checkDocument():
            print(self.document.toxml())

    def PrintBookList(self, tags):
        if not self.checkDocument():
            return None

        bookList = self.document.childNodes
        book = bookList[0].childNodes
        for item in book:
            if item.nodeName == 'book':
                subitems = item.childNodes
                for elem in subitems:
                    if elem.nodeName in tags:
                        print("title=", elem.firstChild.nodeValue)

    def SearchBookTilte(self,keyword):
        if not self.checkDocument():
            return None

        retList = []

        try:
            tree = ElementTree.fromstring(str(self.document.toxml()))
        except Exception:
            print("Element Tree Parsing Error")
            return None

        bookElements = tree.getiterator("book")
        for item in bookElements:
            strTitle = item.find("title")
            if (strTitle.text.find(keyword) >= 0):
                retList.append((item.attrib["ISBN"], strTitle.text))

        return retList

    def checkDocument(self):
        if self.document is None:
            print("Error : Document is empty...")
            return False
        return True

