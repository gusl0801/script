# 검색할 도서 키워드
import sys
import DaumAPIServer
import OpenAPIServer
from tkinter import *
from tkinter import font
from Main import LibSearchButtonHandler
from Mail import *

from MultiLineListBox import MutliLine_Single

radioButtonVar = None
class InterfaceManager:
    def __init__(self, title, pos, color = 'gray'):
        self.window = None
        self.title = title
        self.pos = pos
        self.windowBgColor = color

        self.buttons = []
        self.entries = []
        self.radioButtons = []
        self.List = []

    def AllCreates(self):
        self.CreateWindow()
        self.CreateButtons()
        self.CreateEntries()
        self.CreateRadioButtons()
        self.CreateList()

    def AllRegist(self):
        self.RegistButtons()
        self.RegistEntries()
        self.RegistRadioButtons()
        self.RegistList()

    def CreateWindow(self):
        global radioButtonVar
        self.window = Tk()
        radioButtonVar = IntVar()
        self.window.title(self.title)
        self.window.geometry(self.pos)
        self.window.config(bg = self.windowBgColor)
        self.OffResizable()

    def StartLoop(self):
        self.window.mainloop()

    def OffResizable(self):
        self.window.resizable(0, 0)

    def CreateButtons(self):
        self.buttons.append(InterfaceButton(self.window, (151,70), '      검색      '))
        self.buttons.append(InterfaceButton(self.window, (247,70), ' 도서관 찾기 '))
        self.buttons.append(InterfaceButton(self.window, (20, 70), ' 메일 전송 '))

        for button in self.buttons:
            button.Create()

        self.buttons[2].setHandlerFunc(SendMail)

    def CreateEntries(self):
        self.entries.append(InterfaceEntry(self.window, (150,40), ""))

        for entry in self.entries:
            entry.Create()

    def CreateRadioButtons(self):
        self.radioButtons.append(InterfaceRadioButton(self.window, (150, 10),"제목"))
        self.radioButtons.append(InterfaceRadioButton(self.window, (217, 10), "저자"))
        self.radioButtons.append(InterfaceRadioButton(self.window, (278, 10), "isbn"))
        for radioButton in self.radioButtons:
            radioButton.Create()

    def CreateList(self):
        self.List.append(InterfaceList(self.window, (10, 105), ""))

        for l in self.List:
            l.Create()

    def RegistButtons(self):
        for button in self.buttons:
            button.Regist()
            button.setConnection2Entry(self.entries[0])
            button.setConnections(self.radioButtons)
            button.setConnection2List(self.List[0])

    def RegistEntries(self):
        for entry in self.entries:
            entry.Regist()

    def RegistRadioButtons(self):
        for radioButton in self.radioButtons:
            radioButton.Regist()

    def RegistList(self):
        for l in self.List:
            l.Regist()

    def AppendBookData(self, elements, idx = 0):
        self.List[0]

class Interface:
    def __init__(self, parent, pos, text):
        self.parent = parent
        self.pos = pos
        self.text = text

        self.interface = None

    def handlerFunc(self):
        pass

    def Create(self):
        pass

    def Regist(self):
        pass

    def getData(self):
        return self.interface.get()

class InterfaceButton(Interface):
    ID = 0
    def __init__(self, parent, pos, text):
        super().__init__(parent,pos,text)
        self.connEntry = None
        self.radioButtons = []
        self.connList = None
        self.id = InterfaceButton.ID
        InterfaceButton.ID += 1

    def setHandlerFunc(self,func):
        self.interface.config(command = func)

    def handlerFunc(self):
        if self.id == 0:
            result = []
            sel = self.radioButtons[0].getData()
            if self.connEntry.getData() != '':
                if sel == 0:
                    result = DaumAPIServer.getBookData(query='title', keyword=self.connEntry.getData())
                elif sel == 1:
                    result = DaumAPIServer.getBookData(query='author', keyword=self.connEntry.getData())
                elif sel == 2:
                    result = DaumAPIServer.getBookData(query='isbn', keyword=self.connEntry.getData())
            if len(result) != 0:
                self.connList.clear()
                print(len(result))
                self.connList.AddBookElements(result)

        elif self.id == 1:
            print(type(self.connList))
            print(self.connList.getData())
            print(type(self.connList.getData()))
            data = self.connList.getData()
            index = data.find("title")
            if index != -1:
                #print("found")
                #print(data[index + 8:])
                d = data[index + 8: -4]

                data = LibSearchButtonHandler(data[index + 8: -4])
                print(type(data))
                if data != None:
                    self.connList.AddLibDataDom(data)

                else:
                    print("nope")

            # LibSearchButtonHandler('도둑')


    def Create(self):
        self.interface = Button(self.parent, command = self.handlerFunc)
        pass

    def Regist(self):
        #self.interface.grid(column = self.pos[0], row = self.pos[1])
        self.interface.place(x = self.pos[0], y= self.pos[1])
        self.interface['text'] = self.text
        pass

    def setConnection2Entry(self, interface):
        self.connEntry = interface

    def setConnection2List(self, interface):
        self.connList = interface

    def setConnections(self, interfaces):
        for interface in interfaces:
            self.radioButtons.append(interface)

    #def getDataFromConnList(self):
        #self.connList.get

class InterfaceEntry(Interface):
    def __init__(self, parent, pos, text):
        super().__init__(parent,pos,text)

    def handlerFunc(self):
        pass

    def Create(self):
        self.interface = Entry(self.parent, width = 25)
        pass

    def Regist(self):
        #self.interface.grid(column = self.pos[0], row = self.pos[1])
        self.interface.place(x = self.pos[0], y= self.pos[1])
        self.interface['text'] = self.text
        pass

class InterfaceRadioButton(Interface):
    selection = 1

    #var.set(None)
    count = 0
    def __init__(self, parent, pos, text):
        super().__init__(parent,pos,text)

    def handlerFunc(self):
        return radioButtonVar.get()

    def Create(self):
        self.interface = Radiobutton(self.parent, var = radioButtonVar, value = InterfaceRadioButton.count, command = self.handlerFunc)
        InterfaceRadioButton.count += 1
        pass

    def Regist(self):
        #self.interface.grid(column = self.pos[0], row = self.pos[1])
        self.interface.place(x = self.pos[0], y= self.pos[1])
        self.interface['text'] = self.text
        self.interface.config()
        pass

    def getData(self):
        return self.handlerFunc()

class InterfaceList(Interface):
    def __init__(self, parent, pos, text):
        super().__init__(parent,pos,text)
        self.count = 1

    def handlerFunc(self):
        pass

    def Create(self):
        #480x640
        self.frame = Frame(self.parent, bd=2, relief=RAISED, width=450, height= 500)

        self.scrollbar_ver = Scrollbar(self.frame, orient = 'vertical')
        self.scrollbar_hor = Scrollbar(self.frame, orient = 'horizontal')

        self.lb = MutliLine_Single(self.frame, "", yscrollcommand= self.scrollbar_ver.set,
                                  xscrollcommand=self.scrollbar_hor.set,
                                  width = 60, height = '30', borderwidth = 3, relief = 'groove')

        self.scrollbar_ver.config(command = self.lb._get_lb().yview)
        self.scrollbar_hor.config(command = self.lb._get_lb().xview)
        """
               self.scrollbar = Scrollbar(self.parent)
               self.scrollbar_ = Scrollbar(self.parent, orient = 'horizontal')
               self.scrollbar.pack(fill=Y)

               self.listBox = Listbox(self.parent, activestyle='none',
                                       width = 60, height=30, borderwidth=3, relief='groove',
                                       yscrollcommand=self.scrollbar.set,
                                      xscrollcommand = self.scrollbar_.set)

               self.scrollbar.config(command=self.listBox.yview)
               self.scrollbar_.config(command = self.listBox.xview)
               """

    def Regist(self):
        self.frame.place(x = self.pos[0], y = self.pos[1])
        self.scrollbar_ver.pack(side = RIGHT, fill = Y)

        self.lb.pack()

        self.scrollbar_hor.pack(side = BOTTOM, fill = X)
        #self.lb._place()
        #self.scrollbar.place(x=self.pos[0] + 440, y=self.pos[1])
        #self.scrollbar_.place(x=self.pos[0], y=self.pos[1] + 500)

        """
        self.listBox.place(x = self.pos[0], y = self.pos[1])
        self.scrollbar.place(x = self.pos[0] + 440, y = self.pos[1])
        self.scrollbar_.place(x = self.pos[0], y = self.pos[1] + 500)
        """

        #self.scrollbar.grid(sticky="EW")

    def AddBookElements(self, elemList):
        self.clear()
        for elem in elemList:
            stop = 1
            new_data_flag = False
            text = str()
            for child in elem.childNodes:
                if child.nodeName == 'author' :
                    if child.firstChild != None:
                        text += 'author : ' + str(child.firstChild.data) + '  \n'
                        new_data_flag = True
                elif child.nodeName == 'isbn':
                    if child.firstChild != None:
                        text += 'isbn : ' + str(child.firstChild.data)+ '   \n'
                        new_data_flag = True
                elif child.nodeName == 'title':
                    if child.firstChild != None:
                        text += 'title : ' + str(child.firstChild.data)+ '   \n'
                        new_data_flag = True

            tp = (text, "")
            #self.listBox.insert(self.count, text)
            self.lb._insert(tp)
            self.count += 1

    def AddLibDataDom(self, domList):
        foundNum = 0
        for dom in domList:
            book = dom.getBookListStartPos()
            for item in book:
                if item.nodeName == 'body':
                    bodyNode = item.childNodes
                    for elem in bodyNode:  # items
                        if elem.nodeName == 'items':
                            for itemNode in elem.childNodes:
                                text = str()
                                for data in itemNode.childNodes:
                                    if data.nodeName == 'author':
                                        text += 'author : ' + str(data.firstChild.data) + '  \n'
                                    elif data.nodeName == 'libName':
                                        text += 'libName : ' + str(data.firstChild.data) + '   \n'
                                    elif data.nodeName == 'title':
                                        text += 'title : ' + str(data.firstChild.data) + '   \n'
                                    if foundNum == 0:
                                        self.clear()
                                    foundNum += 1
                                    #print(data.nodeName, "=", data.firstChild.nodeValue)
                                    #print(data.nodeName, "=", data.firstChild.nodeValue, "data : ", data.firstChild.data)
                                tp = (text, "")
                                self.lb._insert(tp)

                                #self.listBox.insert(self.count, text)
                                self.count += 1
        if foundNum != 0:

            print("도서 검색에 성공했습니다.")
            return True
        else:
            print("찾으시는 도서를 소장하고 있는 도서관이 없습니다")
            return False
        """
        bookList = self.document.childNodes
        book = bookList[0].childNodes
        for item in book:
            if item.nodeName == 'body':
                bodyNode = item.childNodes
                for elem in bodyNode:  # items
                    if elem.nodeName == 'items':
                        for itemNode in elem.childNodes:
                            for data in itemNode.childNodes:
                                print(data.nodeName, "=", data.firstChild.nodeValue)
"""
        pass

    def clear(self):
        self.lb._clear_all()
        #self.listBox.delete(0, END)
        #self.count = 1


    def getData(self):
        return self.lb._get_selected_items()
        #sel = self.listBox.curselection()
        #if len(sel) == 1:
        #    data = self.listBox.get(1)
        #    return data

def PrintMenu():
    print("---------검색 기준--------------")
    print("(A/a) --- 소장 도서관")
    print("(S/s) --- 책 이름")
    print("(D/d) --- 책 등록 번호")
    print("(F/f) --- 저작자")
    print("(Z/z) --- 발행자")
    print("(X/x) --- ISBN")
    print("(C/c) --- 발행년도")
    print("(Q/q) --- 프로그램 종료")
    print("--------------------------------")

    return input()

def MenuHandler(sel):
    if sel is 'Q' or sel is 'q':
        sys.exit(1)
    if sel is 'A' or sel is 'a':
        return
    if sel is 'S' or sel is 's':
        return
    if sel is 'D' or sel is 'd':
        return
    if sel is 'F' or sel is 'f':
        return
    if sel is 'Z' or sel is 'z':
        return
    if sel is 'X' or sel is 'x':
        return
    if sel is 'C' or sel is 'c':
        return

def GetKeyword():
    return input("검색 키워드를 입력해주세요")
