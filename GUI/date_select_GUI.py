#导入包
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
import tkinter.font as tkFont
import datetime
import calendar
import sys
sys.path.append('..')
import global_manager as gm

def check_in_date_selection(canvas,check_in_date_sel_text,main_window):
    #定义一些回调函数
    def close_window():
        gm.set_global('check_in_date_window',0)
        check_in_calendar_window.destroy()
    def refresh_dates(calendar_tree,canvas): #翻页刷新日期
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal check_in_select_flag
        #获取当前显示年月
        now_year=int(year_spin.get())
        now_month=int(month_spin.get())
        #异常检测
        if now_year<local_year:
            messagebox.showerror('年份错误','入住年份不能比当前年份前！')
            check_in_calendar_window.wm_attributes('-topmost',True)
            now_year=local_year
            year_spin.delete(0,tk.END)
            year_spin.insert(tk.END,str(now_year))
            if now_month<local_month:
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
        elif now_year==local_year:
            if now_month<local_month:
                messagebox.showerror('月份错误','入住月份不能比当前月份前！')
                check_in_calendar_window.wm_attributes('-topmost',True)
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
        #刷新日历
        refresh_calendar(calendar_tree,canvas,check_in_select_flag)
    def refresh_dates_event(event,calendar_tree,canvas): #直接输入刷新日期
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal check_in_select_flag,canvas_text
        #获取当前显示年月
        now_year=int(year_spin.get())
        now_month=int(month_spin.get())
        #异常检测
        if now_year<local_year:
            messagebox.showerror('年份错误','入住年份不能比当前年份前！')
            check_in_calendar_window.wm_attributes('-topmost',True)
            now_year=local_year
            year_spin.delete(0,tk.END)
            year_spin.insert(tk.END,str(now_year))
            if now_month<local_month:
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
        elif now_year==local_year:
            if now_month<local_month:
                messagebox.showerror('月份错误','入住月份不能比当前月份前！')
                check_in_calendar_window.wm_attributes('-topmost',True)
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
            elif now_month>12:
                messagebox.showerror('月份错误','入住月份不能超过12！')
                check_in_calendar_window.wm_attributes('-topmost',True)
                now_month=12
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
        #刷新日历
        refresh_calendar(calendar_tree,canvas,check_in_select_flag)
    def pressed_calendar(event,calendar_tree,canvas): #选择一个日期
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal temp_check_in_date
        nonlocal check_in_select_flag,canvas_text
        nonlocal calendar_tree_items
        nonlocal press_x,press_y,selection_box
        press_x,press_y,target_widget=event.x,event.y,event.widget
        week_index=target_widget.identify_row(press_y)
        day_index=target_widget.identify_column(press_x)
        if not day_index or not week_index in calendar_tree_items: #单击在行外
            return
        day_value=target_widget.item(week_index,'values')
        if not day_value: #单击在空行
            return
        day_value=day_value[int(day_index[1])-1]
        if not day_value: #日期空
            return
        if now_year==local_year and now_month==local_month and int(day_value)<local_day:
            messagebox.showerror('日期选择错误','入住日期不能在今天之前！')
            check_in_calendar_window.wm_attributes('-topmost',True)
            return
        else:
            check_in_select_flag=1
            now_day=int(day_value)
            temp_check_in_date=[now_year,now_month,now_day]
            #更新画布
            selection_box=target_widget.bbox(week_index,day_index)
            refresh_canvas(canvas,calendar_tree,selection_box,day_value,press_x,press_y)
    def refresh_calendar(calendar_tree,canvas,flag):
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal canvas_text
        nonlocal calendar_tree_items
        nonlocal press_x,press_y,selection_box
        #删除旧日历
        calendar_tree_items=[]
        old_items=calendar_tree.get_children()
        [calendar_tree.delete(item) for item in old_items]
        #加入新日历
        calendar_str=calendar.month(now_year,now_month)
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
            calendar_tree_items.append(calendar_tree.insert('',tk.END,text='',values=this_week_list))
        #更新画布
        if flag:
            if now_year==local_year and now_month==local_month:
                refresh_canvas(canvas,calendar_tree,selection_box,now_day,press_x,press_y)
            else:
                canvas.place_forget()
        check_in_calendar_window.update_idletasks()
    def refresh_canvas(canvas,calendar_tree,bbox,text,x,y):
        nonlocal canvas_text
        canvas.place_forget()
        x,y,width,height=bbox
        text_width=tkFont.Font().measure(text)
        canvas.configure(width=width,height=height)
        canvas.coords(canvas_text,(width-text_width)/2,height/2-1)
        canvas.itemconfigure(canvas_text,text=text)
        canvas.place(in_=calendar_tree,x=x,y=y)
    def confirm_selection(canvas,check_in_sel_text,main_window):
        nonlocal temp_check_in_date
        confirm=messagebox.askyesno('确认选择入住日期','是否确定入住日期为%d年%d月%d日？'%tuple(temp_check_in_date))
        if confirm:
            for index in range(3):
                tmp_element=str(temp_check_in_date[index])
                if len(tmp_element)==1:
                    tmp_element='0'+tmp_element
                temp_check_in_date[index]=tmp_element
            gm.set_global('check_in_date_text','-'.join(temp_check_in_date))
            check_in_calendar_window.destroy()
            gm.set_global('check_in_date_window',0)
            canvas.itemconfig(check_in_date_sel_text,text='入住日期:%s'%gm.get_global('check_in_date_text'))
            main_window.update_idletasks()
        else:
            check_in_calendar_window.wm_attributes('-topmost',True)
    #检查是否已经打开选择窗口
    if gm.get_global('check_in_date_window'):
        return
    #获取当前日期
    temp_check_in_date=datetime.datetime.now().strftime('%Y-%m-%d')
    temp_check_in_date=temp_check_in_date.split('-')
    for index in range(3):
        temp_check_in_date[index]=int(temp_check_in_date[index])
    local_year,local_month,local_day=temp_check_in_date
    #打开新窗口
    check_in_calendar_window=tk.Toplevel()
    check_in_calendar_window.title('入住日期选择')
    check_in_calendar_window.iconbitmap('华南理工大学logo.ico')
    gm.set_global('check_in_date_window',1)
    check_in_calendar_window.protocol("WM_DELETE_WINDOW",close_window)
    #日历控件
        #日历部件初始化
    calendar_tree=Treeview(check_in_calendar_window,selectmode=tk.NONE,show='headings',columns=('SUN','MON','TUE','WED','THU','FRI','SAT'))
    calendar_xingqi_names=['','一','二','三','四','五','六','日']
    calendar_tree_items=[]
    press_x,press_y,selection_box=None,None,None
    for starshine in range(8):
        calendar_tree.heading('#%d'%starshine,text=calendar_xingqi_names[starshine])
        calendar_tree.column('#%d'%starshine,width=30,anchor=tk.CENTER)
        #定义日历画布
    calendar_canvas=tk.Canvas(calendar_tree,background='lightcyan',borderwidth=0,highlightthickness=0)
    canvas_text=calendar_canvas.create_text(0,0,text=str(local_day),fill='deepskyblue',anchor=tk.W)
        #顶部：年月
    now_year,now_month,now_day=temp_check_in_date
    year_spin=tk.Spinbox(check_in_calendar_window,from_=now_year,to_=now_year+20,command=lambda:refresh_dates(calendar_tree,calendar_canvas),width=8)
    month_spin=tk.Spinbox(check_in_calendar_window,from_=1,to_=12,command=lambda:refresh_dates(calendar_tree,calendar_canvas),width=8)
    year_spin.bind('<Return>',lambda event:refresh_dates_event(event,calendar_tree=calendar_tree,canvas=calendar_canvas))
    month_spin.bind('<Return>',lambda event:refresh_dates_event(event,calendar_tree=calendar_tree,canvas=calendar_canvas))
    year_spin.grid(row=0,column=0)
    month_spin.grid(row=0,column=1)
        #中间：日历显示
    check_in_select_flag=0
    refresh_calendar(calendar_tree,calendar_canvas,check_in_select_flag)
    calendar_tree.bind('<Button-1>',lambda event:pressed_calendar(event,calendar_tree=calendar_tree,canvas=calendar_canvas))
    calendar_tree.grid(row=1,column=0,columnspan=2,pady=2)
        #下面：按钮
    confirm_button=tk.Button(check_in_calendar_window,text='确认',font=('华文中宋',14),command=lambda:confirm_selection(canvas,check_in_date_sel_text,main_window))
    confirm_button.grid(row=2,column=0,columnspan=2,pady=1,padx=5)

def check_out_date_selection(canvas,check_out_date_sel_text,main_window):
    #定义一些回调函数
    def close_window():
        gm.set_global('check_out_date_window',0)
        check_out_calendar_window.destroy()
    def refresh_dates(calendar_tree,canvas): #翻页刷新日期
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal check_out_select_flag
        #获取当前显示年月
        now_year=int(year_spin.get())
        now_month=int(month_spin.get())
        #异常检测
        if now_year<local_year:
            messagebox.showerror('年份错误','离店年份不能比当前年份前！')
            check_out_calendar_window.wm_attributes('-topmost',True)
            now_year=local_year
            year_spin.delete(0,tk.END)
            year_spin.insert(tk.END,str(now_year))
            if now_month<local_month:
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
        elif now_year==local_year:
            if now_month<local_month:
                messagebox.showerror('月份错误','离店月份不能比当前月份前！')
                check_out_calendar_window.wm_attributes('-topmost',True)
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
        #刷新日历
        refresh_calendar(calendar_tree,canvas,check_out_select_flag)
    def refresh_dates_event(event,calendar_tree,canvas): #直接输入刷新日期
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal check_out_select_flag,canvas_text
        #获取当前显示年月
        now_year=int(year_spin.get())
        now_month=int(month_spin.get())
        #异常检测
        if now_year<local_year:
            messagebox.showerror('年份错误','离店年份不能比当前年份前！')
            check_out_calendar_window.wm_attributes('-topmost',True)
            now_year=local_year
            year_spin.delete(0,tk.END)
            year_spin.insert(tk.END,str(now_year))
            if now_month<local_month:
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
        elif now_year==local_year:
            if now_month<local_month:
                messagebox.showerror('月份错误','离店月份不能比当前月份前！')
                check_out_calendar_window.wm_attributes('-topmost',True)
                now_month=local_month
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))
            elif now_month>12:
                messagebox.showerror('月份错误','离店月份不能超过12！')
                now_month=12
                month_spin.delete(0,tk.END)
                month_spin.insert(tk.END,str(now_month))   
        #刷新日历
        refresh_calendar(calendar_tree,canvas,check_out_select_flag)
    def pressed_calendar(event,calendar_tree,canvas): #选择一个日期
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal temp_check_out_date
        nonlocal check_out_select_flag,canvas_text
        nonlocal calendar_tree_items
        nonlocal press_x,press_y,selection_box
        press_x,press_y,target_widget=event.x,event.y,event.widget
        week_index=target_widget.identify_row(press_y)
        day_index=target_widget.identify_column(press_x)
        if not day_index or not week_index in calendar_tree_items: #单击在行外
            return
        day_value=target_widget.item(week_index,'values')
        if not day_value: #单击在空行
            return
        day_value=day_value[int(day_index[1])-1]
        if not day_value: #日期空
            return
        if now_year==local_year and now_month==local_month and int(day_value)<local_day:
            messagebox.showerror('日期选择错误','离店日期不能在今天之前！')
            check_out_calendar_window.wm_attributes('-topmost',True)
            return
        else:
            check_out_select_flag=1
            now_day=int(day_value)
            temp_check_out_date=[now_year,now_month,now_day]
            #更新画布
            selection_box=target_widget.bbox(week_index,day_index)
            refresh_canvas(canvas,calendar_tree,selection_box,day_value,press_x,press_y)
    def refresh_calendar(calendar_tree,canvas,flag):
        nonlocal now_year,now_month,now_day
        nonlocal local_year,local_month,local_day
        nonlocal canvas_text
        nonlocal calendar_tree_items
        nonlocal press_x,press_y,selection_box
        #删除旧日历
        calendar_tree_items=[]
        old_items=calendar_tree.get_children()
        [calendar_tree.delete(item) for item in old_items]
        #加入新日历
        calendar_str=calendar.month(now_year,now_month)
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
            calendar_tree_items.append(calendar_tree.insert('',tk.END,text='',values=this_week_list))
        #更新画布
        if flag:
            if now_year==local_year and now_month==local_month:
                refresh_canvas(canvas,calendar_tree,selection_box,now_day,press_x,press_y)
            else:
                canvas.place_forget()
        check_out_calendar_window.update_idletasks()
    def refresh_canvas(canvas,calendar_tree,bbox,text,x,y):
        nonlocal canvas_text
        canvas.place_forget()
        x,y,width,height=bbox
        text_width=tkFont.Font().measure(text)
        canvas.configure(width=width,height=height)
        canvas.coords(canvas_text,(width-text_width)/2,height/2-1)
        canvas.itemconfigure(canvas_text,text=text)
        canvas.place(in_=calendar_tree,x=x,y=y)
    def confirm_selection(canvas,check_out_sel_text,main_window):
        nonlocal temp_check_out_date
        nonlocal now_year,now_month,now_day
        #异常检查
        check_in_date_text=gm.get_global('check_in_date_text')
        if len(check_in_date_text)>3:
                check_in_date_list=check_in_date_text.split('-')
                for tmp_index in range(3):
                    check_in_date_list[tmp_index]=int(check_in_date_list[tmp_index])
                check_in_year,check_in_month,check_in_day=check_in_date_list
                if now_year<check_in_year:
                    messagebox.showerror('日期选择错误','离店日期不能在入住日期之前！')
                    check_out_calendar_window.wm_attributes('-topmost',True)
                    return
                elif now_year==check_in_year:
                    if now_month<check_in_month:
                        messagebox.showerror('日期选择错误','离店日期不能在入住日期之前！')
                        check_out_calendar_window.wm_attributes('-topmost',True)
                        return
                    elif now_month==check_in_month:
                        if now_day<check_in_day:
                            messagebox.showerror('日期选择错误','离店日期不能在入住日期之前！')
                            check_out_calendar_window.wm_attributes('-topmost',True)
                            return
                        elif now_day==check_in_day:
                            messagebox.showerror('日期选择错误','离店日期不能在入住日期相同！')
                            check_out_calendar_window.wm_attributes('-topmost',True)
                            return
        confirm=messagebox.askyesno('确认选择离店日期','是否确定离店日期为%d年%d月%d日？'%tuple(temp_check_out_date))
        if confirm:
            for index in range(3):
                tmp_element=str(temp_check_out_date[index])
                if len(tmp_element)==1:
                    tmp_element='0'+tmp_element
                temp_check_out_date[index]=tmp_element
            gm.set_global('check_out_date_text','-'.join(temp_check_out_date))
            check_out_calendar_window.destroy()
            gm.set_global('check_out_date_window',0)
            canvas.itemconfig(check_out_date_sel_text,text='离店日期:%s'%gm.get_global('check_out_date_text'))
            main_window.update_idletasks()
        else:
            check_out_calendar_window.wm_attributes('-topmost',True)
    #检查是否已经打开选择窗口
    if gm.get_global('check_out_date_window'):
        return
    #获取当前日期
    temp_check_out_date=datetime.datetime.now().strftime('%Y-%m-%d')
    temp_check_out_date=temp_check_out_date.split('-')
    for index in range(3):
        temp_check_out_date[index]=int(temp_check_out_date[index])
    local_year,local_month,local_day=temp_check_out_date
    #打开新窗口
    check_out_calendar_window=tk.Toplevel()
    check_out_calendar_window.title('离店日期选择')
    check_out_calendar_window.iconbitmap('华南理工大学logo.ico')
    gm.set_global('check_out_date_window',1)
    check_out_calendar_window.protocol('WM_DELETE_WINDOW',close_window)
    #日历控件
        #日历部件初始化
    calendar_tree=Treeview(check_out_calendar_window,selectmode=tk.NONE,show='headings',columns=('SUN','MON','TUE','WED','THU','FRI','SAT'))
    calendar_xingqi_names=['','一','二','三','四','五','六','日']
    calendar_tree_items=[]
    press_x,press_y,selection_box=None,None,None
    for starshine in range(8):
        calendar_tree.heading('#%d'%starshine,text=calendar_xingqi_names[starshine])
        calendar_tree.column('#%d'%starshine,width=30,anchor=tk.CENTER)
        #定义日历画布
    calendar_canvas=tk.Canvas(calendar_tree,background='lightcyan',borderwidth=0,highlightthickness=0)
    canvas_text=calendar_canvas.create_text(0,0,text=str(local_day),fill='deepskyblue',anchor=tk.W)
        #顶部：年月
    now_year,now_month,now_day=temp_check_out_date
    year_spin=tk.Spinbox(check_out_calendar_window,from_=now_year,to_=now_year+20,command=lambda:refresh_dates(calendar_tree,calendar_canvas),width=8)
    month_spin=tk.Spinbox(check_out_calendar_window,from_=1,to_=12,command=lambda:refresh_dates(calendar_tree,calendar_canvas),width=8)
    year_spin.bind('<Return>',lambda event:refresh_dates_event(event,calendar_tree=calendar_tree,canvas=calendar_canvas))
    month_spin.bind('<Return>',lambda event:refresh_dates_event(event,calendar_tree=calendar_tree,canvas=calendar_canvas))
    year_spin.grid(row=0,column=0)
    month_spin.grid(row=0,column=1)
        #中间：日历显示
    check_out_select_flag=0
    refresh_calendar(calendar_tree,calendar_canvas,check_out_select_flag)
    calendar_tree.bind('<Button-1>',lambda event:pressed_calendar(event,calendar_tree=calendar_tree,canvas=calendar_canvas))
    calendar_tree.grid(row=1,column=0,columnspan=2,pady=2)
        #下面：按钮
    confirm_button=tk.Button(check_out_calendar_window,text='确认',font=('华文中宋',14),command=lambda:confirm_selection(canvas,check_out_date_sel_text,main_window))
    confirm_button.grid(row=2,column=0,columnspan=2,pady=1,padx=5)