#导入包
import tkinter as tk
from PIL import Image,ImageTk

#打开窗体
main_window=tk.Tk()

#调整窗体属性
main_window.title('Python语言程序设计大作业系统答辩展示-酒店信息爬虫比对系统')
main_window.iconbitmap('华南理工大学logo.ico')
    #设置背景
background_image=Image.open('背景图片.png')
background_image_tk=ImageTk.PhotoImage(background_image)
background_label=tk.Label(main_window)
background_label['image']=background_image_tk
background_label.Image=background_image_tk
        #调整背景图像大小
def change_background_image_size(event):
    global background_image
    background_image=background_image.resize((event.width,event.height),Image.ANTIALIAS)
    background_image_tk=ImageTk.PhotoImage(background_image)
    background_label['image']=background_image_tk
    background_label.Image=background_image_tk
background_label.bind('<Configure>',change_background_image_size)
background_label.pack(fill=tk.BOTH,expand=tk.YES)
main_window.resizable(True,True)

#最上面的标题
transparent_label_background=Image.open('透明图片.jpg')
transparent_label_background_tk=ImageTk.PhotoImage(transparent_label_background)
largest_title_label=tk.Label(main_window,text='携程-去哪儿 酒店信息联查比对系统',fg='yellow',font='幼圆 25 bold',image=transparent_label_background_tk)
largest_title_label.place(relx=0.1,rely=0.1)

#启动窗体
main_window.mainloop()