from tkinter import *

a=['사과','딸기','포도','수박']

def sel():
    select="당신이 선택한 과일은 ?"+a[var.get()]
    label.config(text=select)
r=Tk()
var=IntVar()

for i in range(0,4):
    Radiobutton(r,text=str(i)+'.'+a[i],
                value=i,
                variable=var,
                command=sel).pack(anchor='c')
label=Label(r)
label.pack()
r.mainloop()