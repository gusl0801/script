from tkinter import *

root = Tk()

frame = Frame(bd=2, relief=RAISED, width=80, height=80)

#frame.place(x = 10, y = 10)
frame.pack()
lb = Listbox(frame)
lb.pack(side = LEFT)

sb = Scrollbar(frame)
sb.pack(side = RIGHT, fill = Y)

#self.scrollbar.place(x=self.pos[0] + 440, y=self.pos[1])
#self.scrollbar_.place(x=self.pos[0], y=self.pos[1] + 500

root.geometry('400x400+100+100')
root.mainloop()