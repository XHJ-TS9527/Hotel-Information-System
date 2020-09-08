#导入包
    #系统模块
import tkinter as tk
from tkinter.ttk import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sys
sys.path.append('..')
    #自定义模块
import city_select_GUI
import date_select_GUI
import consult_hotel_GUI
import global_manager as gm
import 爬虫.simulation_explorer_driver as sim_driver
#关闭窗体时操作
def close_main_window():
    #关闭浏览器
    messagebox.showinfo('温馨提示','后台正在进行一些操作,这可能会花费您一些时间来关闭窗口！')
    if gm.get_global('ctrip_open_flag'):
        sim_driver.exit_explorer_driver(gm.get_global('ctrip_driver'))
        gm.del_global('ctrip_driver')
        gm.set_global('ctrip_open_flag',False)
    if gm.get_global('qunar_open_flag'):
        sim_driver.exit_explorer_driver(gm.get_global('qunar_driver'))
        gm.del_global('qunar_driver')
        gm.set_global('qunar_open_flag',False)
    main_window.destroy()
#打开窗体
main_window=tk.Tk()
gm.initial_global_dict()
#调整窗体属性
main_window.title('Python语言程序设计大作业系统答辩展示-酒店信息爬虫比对系统')
main_window.iconbitmap('华南理工大学logo.ico')
main_window.state('zoomed')
main_window.resizable(True,True)
#画布
canvas=tk.Canvas(main_window,borderwidth=0)
canvas.pack(fill=tk.BOTH,expand=tk.YES)
#设置背景
background_image=Image.open('背景图片-白天.png')
background_image_tk=ImageTk.PhotoImage(background_image)
canvas.create_image(610,400,image=background_image_tk,anchor='center')
#调整背景图像大小
# def change_background_image_size(event):
#     global background_image
#     background_image=background_image.resize((event.width,event.height),Image.ANTIALIAS)
#     background_image_tk=ImageTk.PhotoImage(background_image)
#     canvas.create_image(800,200,image=background_image_tk,anchor='center')
#添加大标题
canvas.create_text(680,55,text='携程-去哪儿 酒店信息联查比对系统',fill='yellow',font=('方正字迹-快意体 简',30))
#城市选择
gm.set_global('city_text','请选择')
gm.set_global('city_window',0)
city_sel_text=canvas.create_text(100,120,text='入住城市:%s'%gm.get_global('city_text'),fill='gold',font=('幼圆',20,'bold'),anchor=tk.W)
city_selecbutton=tk.Button(main_window,text='选择城市',font=('华文中宋',14),command=lambda:city_select_GUI.city_selection(canvas,city_sel_text,main_window))
city_selecbutton.place(relx=0.3,rely=0.145)
#入住日期选择
gm.set_global('check_in_date_text','请选择')
gm.set_global('check_in_date_window',0)
check_in_date_sel_text=canvas.create_text(530,120,text='入住日期:%s'%gm.get_global('check_in_date_text'),fill='lime',font=('幼圆',20,'bold'),anchor=tk.W)
check_in_date_selection_button=tk.Button(main_window,text='选择入住',font=('华文中宋',14),command=lambda:date_select_GUI.check_in_date_selection(canvas,check_in_date_sel_text,main_window))
check_in_date_selection_button.place(relx=0.6,rely=0.145)
#离店日期选择
gm.set_global('check_out_date_text','请选择')
gm.set_global('check_out_date_window',0)
check_out_date_sel_text=canvas.create_text(930,120,text='离店日期:%s'%gm.get_global('check_out_date_text'),fill='khaki',font=('幼圆',20,'bold'),anchor=tk.W)
check_out_date_selection_button=tk.Button(main_window,text='选择离店',font=('华文中宋',14),command=lambda:date_select_GUI.check_out_date_selection(canvas,check_out_date_sel_text,main_window))
check_out_date_selection_button.place(relx=0.9,rely=0.145)
#目的地输入
gm.set_global('destination_text','')
canvas.create_text(100,165,text='目的地:',fill='orange',font=('幼圆',20,'bold'),anchor=tk.W)
destination_inputbox=tk.Entry(main_window,text='',width=20)
destination_inputbox.place(relx=0.15,rely=0.22)
#查询数量
def consult_number_spin_callback():
    try:
        consult_number=int(consult_number_spin.get())
    except:
        messagebox.showerror('查询数量有误','请输入合法整数！')
        return
    if consult_number<1:
        messagebox.showerror('查询数量有误','请输入大于0的查询数量！')
        return
    gm.set_global('total_number',consult_number)
def consult_number_spin_callback_event(evnet):
    consult_number_spin_callback()
gm.set_global('total_number',10)
canvas.create_text(430,165,text='查询酒店数量:',fill='turquoise',font=('幼圆',20,'bold'),anchor=tk.W)
consult_number_spin=tk.Spinbox(main_window,from_=1,to=500,increment=1,width=5,command=consult_number_spin_callback)
consult_number_spin.bind('<Return>',consult_number_spin_callback_event)
consult_number_spin.bind('<Leave>',consult_number_spin_callback_event)
consult_number_spin.place(relx=0.46,rely=0.22)
#查询网站选择
def ctrip_check_button_callback():
    global consult_ctrip
    if not gm.get_global('consult_qunar') and not consult_ctrip.get():
        messagebox.showerror('网站选择','请至少选择一个查询网站！')
        consult_ctrip.set(1)
        return
    if consult_ctrip.get():
        gm.set_global('consult_ctrip',True)
    else:
        gm.set_global('consult_ctrip',False)
def qunar_check_button_callback():
    global consult_qunar
    if not gm.get_global('consult_ctrip') and not consult_qunar.get():
        messagebox.showerror('网站选择','请至少选择一个查询网站！')
        consult_qunar.set(1)
        return
    if consult_qunar.get():
        gm.set_global('consult_qunar',True)
    else:
        gm.set_global('consult_qunar',False)
canvas.create_text(730,165,text='查询网站:',fill='orangered',font=('幼圆',20,'bold'),anchor=tk.W)
gm.set_global('consult_ctrip',True)
gm.set_global('consult_qunar',True)
consult_ctrip=tk.IntVar()
consult_qunar=tk.IntVar()
consult_ctrip.set(1)
consult_qunar.set(1)
ctrip_image=Image.open('携程logo.png')
ctrip_image_tk=ImageTk.PhotoImage(ctrip_image)
canvas.create_image(950,161,image=ctrip_image_tk)
qunar_image=Image.open('去哪儿logo.png')
qunar_image_tk=ImageTk.PhotoImage(qunar_image)
canvas.create_image(1100,161,image=qunar_image_tk)
ctrip_consult_checkbox=tk.Checkbutton(main_window,variable=consult_ctrip,bg='dodgerblue',bd=0,command=ctrip_check_button_callback,anchor=tk.CENTER)
ctrip_consult_checkbox.place(relx=0.64,rely=0.21)
qunar_consult_checkbox=tk.Checkbutton(main_window,variable=consult_qunar,bg='goldenrod',bd=0,command=qunar_check_button_callback,anchor=tk.CENTER)
qunar_consult_checkbox.place(relx=0.75,rely=0.21)
#查询结果
    #结果树及其框架
canvas.create_text(800,220,text='查询结果',fill='yellow',font=('幼圆',20,'bold'))
result_show_tree_frame=tk.Frame(main_window,width=930,height=400)
result_show_tree=Treeview(result_show_tree_frame,selectmode=tk.EXTENDED,columns=('item_detail'),height=15)
result_show_tree.heading('#0',text='项目')
result_show_tree.column('#0',anchor=tk.CENTER,width=300)
result_show_tree.heading('#1',text='详细信息')
result_show_tree.column('#1',anchor=tk.CENTER,width=630)
result_show_tree.pack(side=tk.LEFT,fill=tk.Y)
result_show_tree_scrollbar=tk.Scrollbar(result_show_tree_frame)
result_show_tree_scrollbar.pack(side=tk.LEFT,fill=tk.Y)
result_show_tree_scrollbar.config(command=result_show_tree.yview)
result_show_tree.configure(yscrollcommand=result_show_tree_scrollbar.set)
result_show_tree_frame.place(relx=0.27,rely=0.35)
    #结果查询函数
def consult_hotels(destination_text,result_show_tree,main_window):
    #查询酒店
    consult_hotel_GUI.consult_hotels(destination_text)
    shown_hotels=gm.get_global('consulted_hotels')
    #更新结果树
        #清空树中全部项目
    old_items=result_show_tree.get_children()
    [result_show_tree.delete(item) for item in old_items]
        #加入新查询得到的酒店
    result_show_tree.tag_configure('evenColor',background='lightpink')
    result_show_tree.tag_configure('hotelColor',background='lawngreen')
    for each_hotel in shown_hotels:
        print(each_hotel)
        Style().configure('Treeview',row_height=500)
        tag_hotel_name=result_show_tree.insert('',index=tk.END,text=each_hotel['Name'],tag=('hotelColor'))
        row_cnt=1
        Style().configure('Treeview',row_height=350)
        for infos in each_hotel.keys():
            if infos=='Name' or infos=='URL':
                continue
            elif infos=='Address Description':
                info_Chinese='地址'
            elif infos=='Price':
                info_Chinese='价格'
            elif infos=='Score':
                info_Chinese='评分'
            elif infos=='Comment':
                info_Chinese='简评'
            elif infos=='Origin':
                info_Chinese='来源'
            else:
                continue
            if row_cnt%2:
                if infos=='Price':
                    result_show_tree.insert(tag_hotel_name,index=tk.END,text=info_Chinese,values='￥%s'%each_hotel[infos])
                else:
                    result_show_tree.insert(tag_hotel_name,index=tk.END,text=info_Chinese,values=each_hotel[infos])
            else:
                if infos=='Price':
                    result_show_tree.insert(tag_hotel_name,index=tk.END,text=info_Chinese,values=each_hotel[infos],tags=('evenColor'))
                else:
                    result_show_tree.insert(tag_hotel_name,index=tk.END,text=info_Chinese,values=each_hotel[infos],tags=('evenColor'))
            row_cnt+=1
        #更新
    main_window.update_idletasks()
#查询按钮
gm.set_global('ctrip_open_flag',False)
gm.set_global('qunar_open_flag',False)
gm.set_global('consulted_hotels',[])
consult_button=tk.Button(main_window,text='查询酒店列表',font=('华文中宋',14),command=lambda:consult_hotels(destination_inputbox.get(),result_show_tree,main_window))
consult_button.place(relx=0.86,rely=0.205)
#运行窗口
main_window.protocol('WM_DELETE_WINDOW',close_main_window)
main_window.mainloop()