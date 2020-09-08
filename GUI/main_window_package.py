#导入包
    #系统包
import tkinter as tk #GUI界面
from tkinter import messagebox
import tkinter.ttk as ttk #更高级的GUI界面
from PIL import Image,ImageTk #图像处理库
import threading #用于多线程处理
import sys
sys.path.append('..')
import global_manager as gm
    #自定义包
import city_select_package
import date_select_package
import consult_progress_package
import setting_package
import spiders.simulation_explorer_driver as sim
        
class main_window_thread(): #主窗口线程
    def __init__(self,root): #建立窗口并刷新
        self.window=root
        #调整窗体属性
        self.window.title('Python程序设计语言大作业答辩展示系统-酒店信息爬虫比对系统')
        self.window.iconbitmap('华南理工大学logo.ico')
        self.window.state('zoomed')
        self.window.resizable(True,True)
        #建立画布
        self.canvas=tk.Canvas(self.window,borderwidth=0)
        self.canvas.pack(fill=tk.BOTH,expand=tk.YES)
        #设置背景
        background_image=Image.open('背景图片-白天.png')
        background_image=ImageTk.PhotoImage(background_image)
        self.canvas.create_image(610,400,image=background_image,anchor=tk.CENTER)
        #添加大标题
        self.canvas.create_text(680,55,text='携程-去哪儿 酒店信息联查比对系统',fill='yellow',font=('方正字迹-快意体 简',30))
        #城市选择按钮
        self.city_text=self.canvas.create_text(100,120,text='入住城市:请选择',fill='gold',font=('幼圆',20,'bold'),anchor=tk.W)
        self.city_select_button=tk.Button(self.window,text='选择城市',font=('华文中宋',14),command=self.city_select)
        self.city_select_button.place(relx=0.3,rely=0.15)
        #入住日期选择按钮
        self.check_in_date_text=self.canvas.create_text(530,120,text='入住日期:请选择',fill='lime',font=('幼圆',20,'bold'),anchor=tk.W)
        self.check_in_date_select_button=tk.Button(self.window,text='选择入住',font=('华文中宋',14),command=self.check_in_date_select)
        self.check_in_date_select_button.place(relx=0.6,rely=0.15)
        #离店日期选择按钮
        self.check_out_date_text=self.canvas.create_text(930,120,text='离店日期:请选择',fill='khaki',font=('幼圆',20,'bold'),anchor=tk.W)
        self.check_out_date_select_button=tk.Button(self.window,text='选择离店',font=('华文中宋',14),command=self.check_out_date_select)
        self.check_out_date_select_button.place(relx=0.9,rely=0.15)
        #目的地输入栏
        self.canvas.create_text(100,165,text='目的地:',fill='orange',font=('幼圆',20,'bold'),anchor=tk.W)
        self.destination_inputbox=tk.Entry(self.window,text='',width=20)
        self.destination_inputbox.bind('<Leave>',self.destination_refresh_event)
        self.destination_inputbox.bind('<Return>',self.destination_refresh_event)
        self.destination_inputbox.place(relx=0.15,rely=0.225)
        #查询数量
        self.canvas.create_text(430,165,text='查询酒店数量:',fill='turquoise',font=('幼圆',20,'bold'),anchor=tk.W)
        self.consult_number_spin=tk.Spinbox(self.window,from_=1,to=500,increment=1,width=5,command=self.consult_number_command)
        self.consult_number_spin.bind('<Leave>',self.consult_number_event)
        self.consult_number_spin.bind('<Return>',self.consult_number_event)
        self.consult_number_spin.delete(0,tk.END)
        self.consult_number_spin.insert(tk.END,'10')
        self.consult_number_spin.place(relx=0.46,rely=0.225)
        #查询网站选择
        self.canvas.create_text(730,165,text='查询网站:',fill='orangered',font=('幼圆',20,'bold'),anchor=tk.W)
        #两个网站的logo
        ctrip_image=Image.open('携程logo.png')
        ctrip_image=ImageTk.PhotoImage(ctrip_image)
        self.canvas.create_image(950,163,image=ctrip_image)
        qunar_image=Image.open('去哪儿logo.png')
        qunar_image=ImageTk.PhotoImage(qunar_image)
        self.canvas.create_image(1100,163,image=qunar_image)
        self.consult_ctrip=tk.IntVar()
        self.consult_qunar=tk.IntVar()
        self.consult_ctrip.set(1)
        self.consult_qunar.set(1)
        self.ctrip_checkbox=tk.Checkbutton(self.window,variable=self.consult_ctrip,bg='dodgerblue',bd=0,command=self.ctrip_consult)
        self.ctrip_checkbox.place(relx=0.64,rely=0.223)
        self.qunar_checkbox=tk.Checkbutton(self.window,variable=self.consult_qunar,bg='goldenrod',bd=0,command=self.qunar_consult)
        self.qunar_checkbox.place(relx=0.75,rely=0.223)
        #概要查询结果
        self.canvas.create_text(850,220,text='查询结果',fill='yellow',font=('幼圆',20,'bold'))
        self.result_show_tree_frame=tk.Frame(self.window,width=930,height=400)
        self.result_show_tree=ttk.Treeview(self.result_show_tree_frame,selectmode=tk.EXTENDED,columns=('item_detail'),height=16)
        self.result_show_tree.heading('#0',text='项目')
        self.result_show_tree.column('#0',anchor=tk.CENTER,width=300)
        self.result_show_tree.heading('#1',text='详细信息')
        self.result_show_tree.column('#1',anchor=tk.CENTER,width=630)
        self.result_show_tree.pack(side=tk.LEFT,fill=tk.Y)
        self.result_show_tree_scrollbar=tk.Scrollbar(self.result_show_tree_frame)
        self.result_show_tree_scrollbar.pack(side=tk.LEFT,fill=tk.Y)
        self.result_show_tree_scrollbar.config(command=self.result_show_tree.yview)
        self.result_show_tree.configure(yscrollcommand=self.result_show_tree_scrollbar.set)
        self.result_show_tree_frame.place(relx=0.27,rely=0.35)
        #查询按钮
        self.consult_button=tk.Button(self.window,text='查询酒店列表',font=('华文中宋',14),command=self.consult_hotels)
        self.consult_button.place(relx=0.86,rely=0.255)
        #搜索历史
        self.canvas.create_text(180,220,text='查询历史',fill='ivory',font=('幼圆',20,'bold'))
        self.consult_history_frame=tk.Frame(self.window)
        self.history_verticle_scrollbar=tk.Scrollbar(self.consult_history_frame,orient=tk.VERTICAL)
        self.history_horizon_scrollbar=tk.Scrollbar(self.consult_history_frame,orient=tk.HORIZONTAL)
        self.consult_history_box=tk.Listbox(self.consult_history_frame,width=20,height=17,
                                            yscrollcommand=self.history_verticle_scrollbar.set,
                                            xscrollcommand=self.history_horizon_scrollbar.set)
        self.history_horizon_scrollbar.config(command=self.consult_history_box.xview)
        self.history_verticle_scrollbar.config(command=self.consult_history_box.yview)
        self.consult_history_box.grid(row=0,column=0)
        self.consult_history_box.bind('<Double-Button-1>',self.history_box_event)
        self.history_verticle_scrollbar.grid(row=0,column=1,sticky=tk.N+tk.S)
        self.history_horizon_scrollbar.grid(row=1,column=0,sticky=tk.W+tk.E)
        self.consult_history_frame.place(relx=0.05,rely=0.35)
        #对比按钮
        self.compare_button=tk.Button(self.window,text='比较酒店',font=('华文中宋',14),command=self.compare_execute)
        self.compare_button.place(relx=0.4,rely=0.9)
        #导出按钮
        self.outport_button=tk.Button(self.window,text='导出比较表',font=('华文中宋',14),command=self.outport_execute)
        self.outport_button.place(relx=0.75,rely=0.9)
        #菜单栏
        self.menubar=tk.Menu(self.window,bg='lightgray')
        self.setting_menubar=tk.Menu(self.menubar,bg='lightgray',tearoff=False)
        self.menubar.add_cascade(label='设置',menu=self.setting_menubar)
        self.setting_menubar.add_command(label='路径设置',command=self.run_settings)
        self.setting_menubar.add_command(label='比对项设置',command=self.comparison_settings)
        self.restart_menubar=tk.Menu(self.setting_menubar,bg='lightgray',tearoff=False)
        self.setting_menubar.add_cascade(label='重启浏览器内核',menu=self.restart_menubar)
        self.restart_menubar.add_command(label='用于查询清单',command=self.restart_driver_cold)
        self.restart_menubar.add_command(label='用于酒店比较',command=self.restart_driver_hot)
        self.menubar.add_command(label='退出',command=self.close_main_window)
        self.window.config(menu=self.menubar)
        #绑定窗口与关闭函数
        self.window.protocol('WM_DELETE_WINDOW',self.close_main_window)
        self.window.mainloop()
    
    def close_main_window(self): #关闭窗口前关掉浏览器防止内存泄漏
        if gm.get_global('ctrip_driver_open') or gm.get_global('qunar_driver_open'): #浏览器还开着，要关掉
            messagebox.showinfo('温馨提示','后台正在进行一些操作,这可能会花费您一些时间来关闭窗口！')
            if gm.get_global('ctrip_driver_open'):
                temp_driver=gm.get_global('ctrip_driver')
                temp_driver.quit()
                gm.set_global('ctrip_driver_open',False)
            if gm.get_global('qunar_driver_open'):
                temp_driver=gm.get_global('qunar_driver')
                temp_driver.quit()
                gm.set_global('qunar_driver_open',False)
        self.window.destroy()
        
    def restart_driver_cold_core(self): #真正浏览器冷重启函数
        try:
            ctrip_driver=gm.get_global('ctrip_driver')
            ctrip_driver.quit()
            qunar_driver=gm.get_global('qunar_driver')
            qunar_driver.quit()
        except:
            pass
        ctrip_driver=sim.consult_webdriver()
        ctrip_driver=ctrip_driver.visit_driver()
        gm.set_global('ctrip_driver',ctrip_driver)
        gm.set_global('ctrip_driver_open',True)
        qunar_driver=sim.consult_webdriver()
        qunar_driver=qunar_driver.visit_driver()
        gm.set_global('qunar_driver',qunar_driver)
        gm.set_global('qunar_driver_open',True)
        messagebox.showinfo('温馨提示','浏览器内核冷重启成功！')
    
    def restart_driver_cold(self): #冷重启浏览器线程
        self.restart_driver_cold_threading=threading.Thread(target=self.restart_driver_cold_core)
        self.restart_driver_cold_threading.setDaemon(True)
        self.restart_driver_cold_threading.start()
    
    def restart_driver_hot_core(self): #真正浏览器热重启函数
        try:
            ctrip_driver=gm.get_global('ctrip_driver')
            ctrip_driver.quit()
            qunar_driver=gm.get_global('qunar_driver')
            qunar_driver.quit()
        except:
            pass
        ctrip_driver=sim.consult_webdriver(True)
        ctrip_driver=ctrip_driver.visit_driver()
        gm.set_global('ctrip_driver',ctrip_driver)
        gm.set_global('ctrip_driver_open',True)
        qunar_driver=sim.consult_webdriver(True)
        qunar_driver=qunar_driver.visit_driver()
        gm.set_global('qunar_driver',qunar_driver)
        gm.set_global('qunar_driver_open',True)
        messagebox.showinfo('温馨提示','浏览器内核热重启成功！')
    
    def restart_driver_hot(self): #热重启浏览器线程
        self.restart_driver_hot_threading=threading.Thread(target=self.restart_driver_hot_core)
        self.restart_driver_hot_threading.setDaemon(True)
        self.restart_driver_hot_threading.start()

    def city_select_core(self): #城市选择真正函数
        gm.set_global('consulted_flag',False)
        city_select_package.city_select_thread(self)
    
    def city_select(self): #城市选择线程
        self.city_select_threading=threading.Thread(target=self.city_select_core)
        self.city_select_threading.setDaemon(True)
        self.city_select_threading.start()
    
    def check_in_date_select_core(self): #入住日期选择真正函数
        gm.set_global('consulted_flag',False)
        date_select_package.check_in_date_thread(self)
    
    def check_in_date_select(self): #入住日期选择线程
        self.check_in_date_select_threading=threading.Thread(target=self.check_in_date_select_core)
        self.check_in_date_select_threading.setDaemon(True)
        self.check_in_date_select_threading.start()
    
    def check_out_date_select_core(self): #离店日期选择真正函数
        gm.set_global('consulted_flag',False)
        date_select_package.check_out_date_thread(self)
    
    def check_out_date_select(self): #离店日期选择线程
        self.check_out_date_select_threading=threading.Thread(target=self.check_out_date_select_core)
        self.check_out_date_select_threading.setDaemon(True)
        self.check_out_date_select_threading.start()
    
    def destination_refresh_core(self): #目的地刷新真正函数
        gm.set_global('consulted_flag',False)
        gm.set_global('temp_destination',self.destination_inputbox.get())
        
    def destination_refresh(self): #目的地输入框有变化线程
        self.destination_refresh_threading=threading.Thread(target=self.destination_refresh_core)
        self.destination_refresh_threading.setDaemon(True)
        self.destination_refresh_threading.start()
        
    def destination_refresh_event(self,event): #目的地文本输入框事件线程
        self.destination_refresh_event_threading=threading.Thread(target=self.destination_refresh_core)
        self.destination_refresh_event_threading.setDaemon(True)
        self.destination_refresh_event_threading.start()
    
    def consult_number_command_core(self): #真正的查询数量刷新函数
        gm.set_global('consulted_flag',False)
        gm.set_global('temp_consult_number',int(self.consult_number_spin.get()))
    
    def consult_number_command(self): #查询数量刷新线程
        self.consult_number_command_threading=threading.Thread(target=self.consult_number_command_core)
        self.consult_number_command_threading.setDaemon(True)
        self.consult_number_command_threading.start()
        
    def consult_number_event_core(self): #真正的查询数量事件刷新函数
        gm.set_global('consulted_flag',False)
        try:
            temp_number=int(self.consult_number_spin.get())
        except:
            messagebox.showerror('输入错误','请输入正整数类型的查询数量！')
            return
        else:
            if temp_number<1:
                messagebox.showerror('输入错误','请输入正整数类型的查询数量！')
                return
            else:
                gm.set_global('temp_consult_number',temp_number)
    
    def consult_number_event(self,event): #查询数量事件线程
        self.consult_number_command_event_threading=threading.Thread(target=self.consult_number_event_core)
        self.consult_number_command_event_threading.setDaemon(True)
        self.consult_number_command_event_threading.start()
    
    def ctrip_consult_core(self): #设置是否查询携程的真正函数
        gm.set_global('consulted_flag',False)
        if self.consult_ctrip.get():
            gm.set_global('temp_consult_ctrip',True)
        else:
            if not self.consult_qunar.get():
                self.consult_ctrip.set(1)
                messagebox.showerror('选择错误','请至少选择一个查询网站！')
            else:
                gm.set_global('temp_consult_ctrip',False)
    
    def ctrip_consult(self): #是否查询携程线程
        self.ctrip_consult_threading=threading.Thread(target=self.ctrip_consult_core)
        self.ctrip_consult_threading.setDaemon(True)
        self.ctrip_consult_threading.start()
    
    def qunar_consult_core(self): #是否查询去哪儿的真正函数
        gm.set_global('consulted_flag',False)
        if self.consult_qunar.get():
            gm.set_global('temp_consult_qunar',True)
        else:
            if not self.consult_ctrip.get():
                self.consult_qunar.set(1)
                messagebox.showerror('选择错误','请至少选择一个查询网站！')
            else:
                gm.set_global('temp_consult_qunar',False)
    
    def qunar_consult(self): #是否查询去哪儿线程
        self.qunar_consult_threading=threading.Thread(target=self.qunar_consult_core)
        self.qunar_consult_threading.setDaemon(True)
        self.qunar_consult_threading.start()
    
    def consult_hotels_core(self): #查询酒店信息的真正函数
        consult_progress_package.consult_hotels_thread(self)
    
    def consult_hotels(self): #查询酒店线程
        consult_hotels_threading=threading.Thread(target=self.consult_hotels_core)
        consult_hotels_threading.setDaemon(True)
        consult_hotels_threading.start()
    
    def history_box_event_core(self): #历史恢复函数
        gm.set_global('consulted_flag',False)
        selected_item=self.consult_history_box.curselection()
        if selected_item:
            selected_index=selected_item[0]
            selected_item=self.consult_history_box.get(selected_index)
            selected_content=selected_item.split(',')
            city=selected_content[0].replace('城市:','')
            gm.set_global('temp_city',city)
            self.canvas.itemconfig(self.city_text,text='入住城市:%s'%city)
            check_in_date=selected_content[1].replace('入住日期:','')
            gm.set_global('temp_check_in_date',check_in_date)
            self.canvas.itemconfig(self.check_in_date_text,text='入住日期:%s'%check_in_date)
            check_out_date=selected_content[2].replace('离店日期:','')
            gm.set_global('temp_check_out_date',check_out_date)
            self.canvas.itemconfig(self.check_out_date_text,text='离店日期:%s'%check_out_date)
            destination=selected_content[3].replace('目的地:','')
            gm.set_global('temp_destination',destination)
            self.destination_inputbox.delete(0,tk.END)
            self.destination_inputbox.insert(tk.END,destination)
            consult_number=int(selected_content[4].replace('查询数量:',''))
            gm.set_global('temp_consult_number',consult_number)
            self.consult_number_spin.delete(0,tk.END)
            self.consult_number_spin.insert(tk.END,str(consult_number))
            consult_websites=selected_content[5].replace('查询网站:','')
            if '|' in consult_websites:
                self.consult_ctrip.set(1)
                self.consult_qunar.set(1)
                gm.set_global('temp_consult_ctrip',True)
                gm.set_global('temp_consult_qunar',True)
            elif consult_websites=='携程网':
                self.consult_ctrip.set(1)
                self.consult_qunar.set(0)
                gm.set_global('temp_consult_ctrip',True)
                gm.set_global('temp_consult_qunar',False)
            else:
                self.consult_ctrip.set(0)
                self.consult_qunar.set(1)
                gm.set_global('temp_consult_ctrip',False)
                gm.set_global('temp_consult_qunar',True)
    
    def history_box_event(self,event): #历史恢复线程
        self.history_event_threading=threading.Thread(target=self.history_box_event_core)
        self.history_event_threading.setDaemon(True)
        self.history_event_threading.start()
    
    def compare_execute_core(self): #真正的比较函数
        consult_progress_package.consult_detail_info_thread(self)
    
    def compare_execute(self): #比较线程
        self.compare_execute_threading=threading.Thread(target=self.compare_execute_core)
        self.compare_execute_threading.setDaemon(True)
        self.compare_execute_threading.start()
        
    def run_settings_core(self): #真正的修改路径函数
        setting_package.set_thread(self)
    
    def run_settings(self): #修改路径线程
        self.run_settings_thread=threading.Thread(target=self.run_settings_core)
        self.run_settings_thread.setDaemon(True)
        self.run_settings_thread.start()
    
    def comparison_settings_core(self): #真正修改对比项的函数
        setting_package.comparison_adjust_thread(self)
    
    def comparison_settings(self): #修改对比项线程
        comparison_settings_threading=threading.Thread(target=self.comparison_settings_core)
        comparison_settings_threading.setDaemon(True)
        comparison_settings_threading.start()
        
    def outport_execute_core(self): #真正的文件导出函数
        setting_package.outport_thread(self)
    
    def outport_execute(self): #导出函数线程
        output_execute_threading=threading.Thread(target=self.outport_execute_core)
        output_execute_threading.setDaemon(True)
        output_execute_threading.start()