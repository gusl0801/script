# 검색할 도서 키워드
import sys
import DaumAPIServer
import OpenAPIServer
from tkinter import *
from tkinter import font
from Main import LibSearchButtonHandler
from Mail import *

from MultiLineListBox import MutliLine_Single
from Mail import MailSender

from io import BytesIO
import urllib.request
from PIL import Image, ImageTk

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
        self.label = []

    def AllCreates(self):
        self.CreateWindow()
        self.CreateButtons()
        self.CreateEntries()
        self.CreateRadioButtons()
        self.CreateList()
        self.CreateLabel()


    def AllRegist(self):
        self.RegistButtons()
        self.RegistEntries()
        self.RegistRadioButtons()
        self.RegistList()
        self.RegistLabel()


        label = Label(self.window, text = "메일 주소 입력 ", bg = 'gray')
        label.place(x = 18, y = 122)

        entry = Entry(self.window, width = 25, bd = 3)
        entry.place(x = 148, y = 120 )


        lb = Listbox(self.window, activestyle='none',
                                width=12, height=3, borderwidth=7, relief= RAISED,)#yscrollcommand=ListBoxScrollbar.set)
        lb.place(x = 350, y = 37)

        label_ = Label(self.window, text="도서관 목록 ", bg = 'gray' )
        label_.place(x=363, y=7)

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
        self.buttons.append(InterfaceButton(self.window, (350, 120), '     메일 전송     '))

        for button in self.buttons:
            button.Create()

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
        self.List.append(InterfaceList(self.window, (10, 155), ""))

        for l in self.List:
            l.Create()
    def CreateLabel(self):
        self.label.append(InterfaceLabel(self.window, (10,5)))

        for l in self.label:
            l.Create()

    def RegistButtons(self):
        for button in self.buttons:
            button.Regist()
            button.setConnection2Entry(self.entries[0])
            button.setConnections(self.radioButtons)
            button.setConnection2List(self.List[0])

        sender = "scoke0801@gmail.com"
        reciver = "scoke0801@daum.net"
        passwd = "dla753156"
        mail_sender = MailSender(sender, reciver, passwd, self.List[0])
        self.buttons[2].setHandlerFunc(mail_sender, mail_sender.Send)

    def RegistEntries(self):
        for entry in self.entries:
            entry.Regist()

    def RegistRadioButtons(self):
        for radioButton in self.radioButtons:
            radioButton.Regist()

    def RegistList(self):
        for l in self.List:
            l.Regist()
        self.List[0].connectLabel(self.label[0])

    def RegistLabel(self):
        for l in self.label:
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

    def setHandlerFunc(self, instance, func):
        self.instance = instance
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
                self.connList.AddBookElements(result)

        elif self.id == 1:
            data = self.connList.getData()
            index = data.find("title")
            if index != -1:
                #print("found")
                #print(data[index + 8:])
                d = data[index + 8: -4]

                data = LibSearchButtonHandler(data[index + 8: -4])

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
        self.connected_label = None

    def handlerFunc(self):
        pass

    def Create(self):
        #480x640
        self.frame = Frame(self.parent, bd=2, relief=RAISED, width=450, height= 400)

        self.scrollbar_ver = Scrollbar(self.frame, orient = 'vertical')
        self.scrollbar_hor = Scrollbar(self.frame, orient = 'horizontal')

        self.lb = MutliLine_Single(self.frame, "", yscrollcommand= self.scrollbar_ver.set,
                                  xscrollcommand=self.scrollbar_hor.set,
                                  width = 60, height = '27', borderwidth = 3, relief = 'groove')

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
        url_list = []
        line_count = 0
        c = 0
        url = None
        find_url = None
        for elem in elemList:
            text = str()
            last_line = 0
            for child in elem.childNodes:
                if child.nodeName == 'author' :
                    if child.firstChild != None:
                        text += 'author : ' + str(child.firstChild.data) + '\n'
                        line_count += 1
                        last_line += 1
                elif child.nodeName == 'isbn':
                    if child.firstChild != None:
                        text += 'isbn : ' + str(child.firstChild.data)+ '\n'
                        line_count += 1
                        last_line += 1
                elif child.nodeName == 'title':
                    if child.firstChild != None:
                        text += 'title : ' + str(child.firstChild.data)+ '\n'
                        line_count += 1
                        last_line += 1
                elif child.nodeName == 'cover_l_url':
                    if child.firstChild != None:
                        line_count += 1
                        last_line += 1
                        find_url = True
                        url = child.firstChild.data
            if find_url is False:
                line_count += 1
            url_list.append((url, line_count - last_line))
            url = None
            find_url = False
            tp = (text, "")
            self.lb._insert(tp)

        if len(url_list) != 0:
            self.connected_label.setUrls(url_list)

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
                                        text += 'author : ' + str(data.firstChild.data) + '\n'
                                    elif data.nodeName == 'libName':
                                        text += 'libName : ' + str(data.firstChild.data) + '\n'
                                    elif data.nodeName == 'title':
                                        text += 'title : ' + str(data.firstChild.data) + '\n'
                                    if foundNum == 0:
                                        self.clear()
                                    foundNum += 1
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

    def connectLabel(self, label):
        self.connected_label = label
        self.lb.connect_label(label)

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
    def getListData(self):
        return self.lb._get_selected_items_list()

class InterfaceLabel(Interface):
    def __init__(self, parent, pos):
        super().__init__(parent,pos, "")
        self.url_list = None

    def handlerFunc(self):
        pass

    def Create(self):
        self.frame = Frame(self.parent, bd = 1, relief=RAISED, width= 100, height= 100, bg = 'gray')

        #self.label = Label(self.frame, height=100, width=100)
        pass

    def Regist(self):
        self.frame.place(x = self.pos[0], y= self.pos[1])
        #self.label.pack()
        #self.label.place(x=0,y=0)


        #self.label.place(x=100,y=100)
        pass

    def PresentImage(self, raw_index):
        index = self.FindIndex(raw_index)

        if index is None:
            return

        url = self.url_list[index][0]
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        image_file = Image.open(BytesIO(raw_data))
        #if image_file is None:
        #    print("연결된 url이미지가 없습니다")
        #    return

        image_file = image_file.resize((100, 100), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image_file)
        self.label = Label(self.frame, image = image, height=105, width=105)
        self.label.image = image
        self.label.pack()
        self.label.place(x=0,y=0)

    def FindIndex(self, raw_index):
        index = 0
        for tp in self.url_list:    # tuple
            if tp[1] == raw_index:
                return index
            index += 1

        return None

    def setUrls(self, url_list):
        self.url_list = url_list

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
