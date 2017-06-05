import MultiLineListBox MultiLineListBox

from tkinter import *

roop = Tk()

lb = Listbox(roop)
lb.pack(side = 'left')
lb.place(x = 30, y = 20)

text = "1234" + "\n" + "5678"

#lb.insert(0, "1234")
#lb.insert(0, "\n")
#lb.insert(0, "4567")

lb.insert(1, "1234"+"\n"+"5678")

lb.insert(2, text)
roop.mainloop()

"""
from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk

root = Tk()
root.geometry("500x500+500+200")

# openapi로 이미지 url을 가져옴.
url = "http://tong.visitkorea.or.kr/cms/resource/74/2396274_image2_1.JPG"
with urllib.request.urlopen(url) as u:
    raw_data = u.read()

im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

label = Label(root, image=image, height=400, width=400)
label.pack()
label.place(x=0, y=0)
root.mainloop()
"""