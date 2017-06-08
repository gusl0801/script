"""

from tkinter import *

window = Tk()
window.geometry('400x400+100+100')
f = Frame(window, width = 400, height = 400)
f.place(x = 150, y = 150)
f.pack()

lBox = Listbox(f)
scr = Scrollbar(window)
scr.config(command=lBox.yview)

lBox.place(x = 60, y = 60)


window.mainloop()
"""
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

    def Regist(self):
        self.listBox.place(x = self.pos[0], y = self.pos[1])
        self.scrollbar.place(x = self.pos[0] + 440, y = self.pos[1])
        self.scrollbar_.place(x = self.pos[0], y = self.pos[1] + 500)
"""
"""
# example code1
from tkinter import *

root = Tk()
frame = Frame(root)
frame.pack()

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

redbutton = Button(frame, text="Red", fg="red")
redbutton.pack( side = LEFT)

greenbutton = Button(frame, text="Brown", fg="brown")
greenbutton.pack( side = LEFT )

bluebutton = Button(frame, text="Blue", fg="blue")
bluebutton.pack( side = LEFT )

blackbutton = Button(bottomframe, text="Black", fg="black")
blackbutton.pack( side = BOTTOM)

topFrame = Frame(root)
topFrame.pack(side = RIGHT)

magentbutton = Button(topFrame, text = "Magenta", fg = "magenta")
magentbutton.config(side = RIGHT)
root.mainloop()
"""

# -*- coding : cp949 -*-
# example code2
from tkinter import *


class MyApp:
    def __init__(self, parent):
        self.myParent = parent

        # ----- myContainer1 -----
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()

        # ----- 조감을 제어하는에 필요한 상수들 -----
        button_width = 6
        button_padx = "2m"
        button_pady = "1m"
        buttons_frame_padx = "3m"
        buttons_frame_pady = "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"
        # ----- 상수 끝 -----

        ### myContainer1안에 수직적 동선을 사용한다.
        ### myContainer1안에 먼저 buttons_frame을 만든 후
        ### top_frame와 bottom_frame를 만든다

        # ----- buttons_frame -----
        self.buttons_frame = Frame(self.myContainer1, background="blue")
        self.buttons_frame.pack(side=TOP,
                                ipadx=buttons_frame_ipadx,
                                ipady=buttons_frame_ipady,
                                padx=buttons_frame_padx,
                                pady=buttons_frame_pady)

        # ----- top_frame -----
        self.top_frame = Frame(self.myContainer1)
        self.top_frame.pack(side=TOP,
                            fill=BOTH,
                            expand=YES)

        # ----- bottom_frame -----
        self.bottom_frame = Frame(self.myContainer1,
                                  borderwidth=5,  # 틀 테두리 두꼐
                                  relief=RIDGE,  # 틀 모양
                                  height=50,  # 틀 높이
                                  background="white")
        self.bottom_frame.pack(side=TOP,
                               fill=BOTH,  # 빈공간 채우기
                               expand=YES)

        ### left_frame과 right_frame이라는
        ### 두개의 틀을 top_frame안에 배치한다.
        ### top_frame안에 수평적동선을 사용한다.

        # ----- left_frame -----
        self.left_frame = Frame(self.top_frame,
                                background="red",
                                borderwidth=5,
                                relief=RIDGE,
                                height=250,
                                width=50)
        self.left_frame.pack(side=LEFT,
                             fill=BOTH,
                             expand=YES)

        # ----- right_frame -----
        self.right_frame = Frame(self.top_frame,
                                 background="tan",
                                 borderwidth=5,
                                 relief=RIDGE,
                                 width=250)
        self.right_frame.pack(side=RIGHT,
                              fill=BOTH,
                              expand=YES)

        ### 버튼들을 buttons_frame에 추가한다.

        # ----- button1 -----
        self.button1 = Button(self.buttons_frame, command=self.button1Click)
        self.button1.bind("<Return>", self.button1Click)
        self.button1.configure(text="OK", background="green",
                               width=button_width,
                               padx=button_padx,
                               pady=button_pady)
        self.button1.focus_force()  # 초기 초점 지정
        self.button1.pack(side=LEFT)

        # ----- button2 -----
        self.button2 = Button(self.buttons_frame, command=self.button2Click)
        self.button2.bind("<Return>", self.button2Click)
        self.button2.configure(text="Cancel", background="red",
                               width=button_width,
                               padx=button_padx,
                               pady=button_pady)
        self.button2.pack(side=RIGHT)

    # ----- Functions -----
    def button1Click(self, event=None):
        if self.button1["background"] == "green":
            self.button1.configure(background="yellow")
        else:
            self.button1.configure(background="green")

    def button2Click(self, event=None):
        self.myParent.destroy()  # 어플리케이션 닫기


root = Tk()
myapp = MyApp(root)
root.mainloop()