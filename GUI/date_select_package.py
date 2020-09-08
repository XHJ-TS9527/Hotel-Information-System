#导入包
import tkinter as tk #GUI
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox #用于提示消息
import threading #多线程
import sys
sys.path.append('..')
import global_manager as gm #全局变量管理器
import calendar #用于获取日历
import datetime #用于获取本地事件

class system_calendar():
    def __init__(self,master):
        self.master=master
        #获取当前时间
        temp_check_in_date=datetime.datetime.now().strftime('%Y-%m-%d')
        temp_check_in_date=temp_check_in_date.split('-')
        self.local_year=int(temp_check_in_date[0])
        self.local_month=int(temp_check_in_date[1])
        self.local_day=int(temp_check_in_date[2])
        self.now_year=self.local_year
        self.now_month=self.local_month
        self.now_day=self.local_day
        self.selected_year=self.local_year
        self.selected_month=self.local_month
        self.selected_day=self.local_day
        #定义顶部年月
        self.year_spin=tk.Spinbox(self.master,from_=self.local_year,to=self.local_year+20,
                                  width=8,command=self.year_spin_callback)
        self.month_spin=tk.Spinbox(self.master,from_=1,to=12,width=8,
                                  command=self.month_spin_callback)
        self.year_spin.bind('<Return>',self.year_spin_event)
        self.month_spin.bind('<Return>',self.month_spin_event)
        self.year_spin.grid(row=0,column=0)
        self.month_spin.grid(row=0,column=1)
        #定义中部的树
        self.calendar_tree=ttk.Treeview(self.master,selectmode=tk.NONE,
                                        show='headings',columns=('MON','TUE','WED','THU','FRI','SAT','SUN'))
        self.weekdays_name=('','一','二','三','四','五','六','日')
        self.calendar_tree_items=[]
        self.press_x,self.press_y=None,None
        self.selection_box=None
        for starshine in range(8):
            self.calendar_tree.heading('#%d'%starshine,text=self.weekdays_name[starshine])
            self.calendar_tree.column('#%d'%starshine,width=30,anchor=tk.CENTER)
        #定义树画布
        self.calendar_canvas=tk.Canvas(self.calendar_tree,background='lightcyan',borderwidth=0,highlightthickness=0)
        self.calendar_canvas_text=self.calendar_canvas.create_text(0,0,text=str(self.local_day),fill='deepskyblue',anchor=tk.W)
        self.checked_flag=False
        self.calendar_tree.bind('<Button-1>',self.pressed_event)
        self.calendar_tree.grid(row=1,column=0,columnspan=2,pady=2)
        
    def refresh_calendar_date(self): #顶部的年月发生变更
        #异常处理
        try:
            self.now_year=int(self.year_spin.get())
        except:
            messagebox.showerror('输入错误','请输入正整数类型的年份！')
            self.master.wm_attributes('-topmost',True)
            return
        else:
            if self.now_year<self.local_year:
                messagebox.showerror('输入错误','输入年份在当前年份之前,已自动调整为当前年份！')
                self.master.wm_attributes('-topmost',True)
                self.year_spin.delete(0,tk.END)
                self.year_spin.insert(tk.END,str(self.local_year))
                self.now_year=self.local_year
            if self.now_year==self.local_year:
                try:
                    self.now_month=int(self.month_spin.get())
                except:
                    messagebox.showerror('输入错误','请输入正整数类型的月份！')
                    self.master.wm_attributes('-topmost',True)
                    return
                else:
                    if self.now_month<self.local_month:
                        messagebox.showerror('输入错误','输入月份在当前月份之前,已自动调整为当前年份！')
                        self.master.wm_attributes('-topmost',True)
                        self.month_spin.delete(0,tk.END)
                        self.month_spin.insert(tk.END,str(self.local_month))
                        self.now_month=self.local_month
            else:
                try:
                    self.now_month=int(self.month_spin.get())
                except:
                    messagebox.showerror('输入错误','请输入正整数类型的月份！')
                    self.master.wm_attributes('-topmost',True)
                    return
        #刷新日历
        self.refresh_calendar()
    
    def refresh_calendar(self): #更新日历面板
        self.calendar_canvas.place_forget() #先删除选中的格子
        #删除旧日历
        old_items=self.calendar_tree.get_children()
        [self.calendar_tree.delete(item) for item in old_items]
        #加入新日历
        self.calendar_tree_items=[]
        calendar_str=calendar.month(self.now_year,self.now_month)
        calendar_strs=calendar_str.split('\n')
        del calendar_strs[0]
        del calendar_strs[0]
        calendar_strs.pop()
        for each_week in calendar_strs:
            this_week_list=each_week.strip().split(' ')
            while '' in this_week_list:
                this_week_list.remove('')
            if len(this_week_list)!=7:
                need_days=7-len(this_week_list)
                temp_this_week=['']*need_days
                if '1' in this_week_list:
                    temp_this_week.extend(this_week_list)
                    this_week_list=temp_this_week
                else:
                    this_week_list.extend(temp_this_week)
            self.calendar_tree_items.append(self.calendar_tree.insert('',tk.END,
                                                                      text='',values=this_week_list))
        #更新画布
        if self.checked_flag:
            if self.now_year==self.selected_year and self.now_month==self.selected_month:
                self.refresh_canvas()
    
    def refresh_canvas(self): #更新选框
        self.calendar_canvas.place_forget()
        x,y,width,height=self.selection_box
        text_width=tkFont.Font().measure(str(self.now_day))
        self.calendar_canvas.configure(width=width,height=height)
        self.calendar_canvas.coords(self.calendar_canvas_text,(width-text_width)/2,height/2-1)
        self.calendar_canvas.itemconfigure(self.calendar_canvas_text,text=str(self.now_day))
        self.calendar_canvas.place(in_=self.calendar_tree,x=x,y=y)
    
    def pressed_calendar(self,*args): #日历点击选取事件
        event=args[0]
        self.press_x,self.press_y,target_widget=event.x,event.y,event.widget
        week_index=target_widget.identify_row(self.press_y)
        day_index=target_widget.identify_column(self.press_x)
        if not day_index or not week_index in self.calendar_tree_items:
            return #单击在行外
        day_value=target_widget.item(week_index,'values')
        if not day_value:
            return #单击在空行
        day_value=day_value[int(day_index[1])-1]
        if not day_value:
            return #日期空
        if self.now_year==self.local_year and self.now_month==self.local_month and int(day_value)<self.local_day:
            messagebox.showerror('选择错误','选择日期不能在今天之前！')
            self.master.wm_attributes('-topmost',True)
            return
        else:
            self.checked_flag=True
            self.now_day=int(day_value)
            self.selected_year=self.now_year
            self.selected_month=self.now_month
            self.selected_day=self.now_day
            self.selection_box=target_widget.bbox(week_index,day_index)
            self.refresh_canvas()
        
    def pressed_event(self,event): #日历点击事件线程
        self.pressed_event_threading=threading.Thread(target=self.pressed_calendar,args=(event,))
        self.pressed_event_threading.setDaemon(True)
        self.pressed_event_threading.start()
    
    def year_spin_callback(self): #年份切换事件线程
        self.year_spin_callback_threading=threading.Thread(target=self.refresh_calendar_date)
        self.year_spin_callback_threading.setDaemon(True)
        self.year_spin_callback_threading.start()
    
    def year_spin_event(self,event): #年份框事件线程
        self.year_spin_callback_threading=threading.Thread(target=self.refresh_calendar_date)
        self.year_spin_callback_threading.setDaemon(True)
        self.year_spin_callback_threading.start()
    
    def month_spin_callback(self): #月份切换事件线程
        self.month_spin_callback_threading=threading.Thread(target=self.refresh_calendar_date)
        self.month_spin_callback_threading.setDaemon(True)
        self.month_spin_callback_threading.start()
        
    def month_spin_event(self,event): #月份框事件线程
        self.month_spin_callback_threading=threading.Thread(target=self.refresh_calendar_date)
        self.month_spin_callback_threading.setDaemon(True)
        self.month_spin_callback_threading.start()

class check_in_date():
    def __init__(self,master):
        self.master=master
        #打开新窗口
        self.window=tk.Toplevel()
        self.window.title('入住日期选择')
        self.window.iconbitmap('华南理工大学logo.ico')
        gm.set_global('check_in_date_window_flag',True)
        self.window.protocol("WM_DELETE_WINDOW",self.close_window)
        #放日历组件
        self.calendar=system_calendar(self.window)
        self.calendar.refresh_calendar()
        #确认按钮组件
        self.confirm_button=tk.Button(self.window,text='确认',font=('华文中宋',14),command=self.confirm)
        self.confirm_button.grid(row=2,column=0,columnspan=2,pady=1,padx=5)
    
    def confirm_core(self): #真正的确认函数
        if not self.calendar.checked_flag:
            messagebox.showerror('选择错误','您还没有选择入住日期！')
            self.window.wm_attributes('-topmost',True)
            return
        if len(gm.get_global('temp_check_out_date'))!=0:
            check_out_date=gm.get_global('temp_check_out_date').split('-')
            check_out_year=int(check_out_date[0])
            check_out_month=int(check_out_date[1])
            check_out_day=int(check_out_date[2])
            if self.calendar.selected_year>check_out_year:
                messagebox.showerror('选择错误','入住日期不能迟于离店日期！')
                self.window.wm_attributes('-topmost',True)
                return
            elif self.calendar.selected_year==check_out_year:
                if self.calendar.selected_month>check_out_month:
                    messagebox.showerror('选择错误','入住日期不能迟于离店日期！')
                    self.window.wm_attributes('-topmost',True)
                    return
                elif self.calendar.selected_month==check_out_month:
                    if self.calendar.selected_day>=check_out_day:
                        messagebox.showerror('选择错误','入住日期不能迟于离店日期！')
                        self.window.wm_attributes('-topmost',True)
                        return
        confirm=messagebox.askyesno('确认选择','是否确定入住日期为%d年%d月%d日？'%(self.calendar.selected_year,
                                     self.calendar.selected_month,self.calendar.selected_day))
        if confirm:
            year_text=str(self.calendar.selected_year)
            if self.calendar.selected_month<10:
                month_text='0'+str(self.calendar.selected_month)
            else:
                month_text=str(self.calendar.selected_month)
            if self.calendar.selected_day<10:
                day_text='0'+str(self.calendar.selected_day)
            else:
                day_text=str(self.calendar.selected_day)
            gm.set_global('temp_check_in_date','-'.join((year_text,month_text,day_text)))
            self.master.canvas.itemconfigure(self.master.check_in_date_text,text='入住日期:%s'%gm.get_global('temp_check_in_date'))
            self.master.window.update_idletasks()
            self.close_window()
        else:
            self.window.wm_attributes('-topmost',True)
        
    def confirm(self): #确认选择线程
        self.confirm_threading=threading.Thread(target=self.confirm_core)
        self.confirm_threading.setDaemon(True)
        self.confirm_threading.start()
            
    def close_window(self):
        gm.set_global('check_in_date_window_flag',False)
        self.window.destroy()
        
class check_out_date():
    def __init__(self,master):
        self.master=master
        #打开新窗口
        self.window=tk.Toplevel()
        self.window.title('离店日期选择')
        self.window.iconbitmap('华南理工大学logo.ico')
        gm.set_global('check_out_date_window_flag',True)
        self.window.protocol("WM_DELETE_WINDOW",self.close_window)
        #放日历组件
        self.calendar=system_calendar(self.window)
        self.calendar.refresh_calendar()
        #确认按钮组件
        self.confirm_button=tk.Button(self.window,text='确认',font=('华文中宋',14),command=self.confirm)
        self.confirm_button.grid(row=2,column=0,columnspan=2,pady=1,padx=5)
    
    def confirm_core(self): #真正的确认函数
        if not self.calendar.checked_flag:
            messagebox.showerror('选择错误','您还没有选择离店日期！')
            self.window.wm_attributes('-topmost',True)
            return
        if len(gm.get_global('temp_check_in_date'))!=0:
            check_in_date=gm.get_global('temp_check_in_date').split('-')
            check_in_year=int(check_in_date[0])
            check_in_month=int(check_in_date[1])
            check_in_day=int(check_in_date[2])
            if self.calendar.selected_year<check_in_year:
                messagebox.showerror('选择错误','离店日期不能早于入住日期！')
                self.window.wm_attributes('-topmost',True)
                return
            elif self.calendar.selected_year==check_in_year:
                if self.calendar.selected_month<check_in_month:
                    messagebox.showerror('选择错误','离店日期不能早于入住日期！')
                    self.window.wm_attributes('-topmost',True)
                    return
                elif self.calendar.selected_month==check_in_month:
                    if self.calendar.selected_day<=check_in_day:
                        messagebox.showerror('选择错误','离店日期不能早于入住日期！')
                        self.window.wm_attributes('-topmost',True)
                        return
        confirm=messagebox.askyesno('确认选择','是否确定离店日期为%d年%d月%d日？'%(self.calendar.selected_year,
                                     self.calendar.selected_month,self.calendar.selected_day))
        if confirm:
            year_text=str(self.calendar.selected_year)
            if self.calendar.selected_month<10:
                month_text='0'+str(self.calendar.selected_month)
            else:
                month_text=str(self.calendar.selected_month)
            if self.calendar.selected_day<10:
                day_text='0'+str(self.calendar.selected_day)
            else:
                day_text=str(self.calendar.selected_day)
            gm.set_global('temp_check_out_date','-'.join((year_text,month_text,day_text)))
            self.master.canvas.itemconfigure(self.master.check_out_date_text,text='离店日期:%s'%gm.get_global('temp_check_out_date'))
            self.master.window.update_idletasks()
            self.close_window()
        else:
            self.window.wm_attributes('-topmost',True)
        
    def confirm(self): #确认选择线程
        self.confirm_threading=threading.Thread(target=self.confirm_core)
        self.confirm_threading.setDaemon(True)
        self.confirm_threading.start()
            
    def close_window(self):
        gm.set_global('check_out_date_window_flag',False)
        self.window.destroy()

def check_in_date_thread(master):
    if not gm.get_global('check_in_calendar_window_flag'):
        temp=check_in_date(master)
        while gm.get_global('check_in_calendar_window_flag'):
            pass
        del temp

def check_out_date_thread(master):
    if not gm.get_global('check_out_calendar_window_flag'):
        temp=check_out_date(master)
        while gm.get_global('check_out_calendar_window_flag'):
            pass
        del temp