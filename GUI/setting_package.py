#导入包
import tkinter as tk #GUI
from tkinter import messagebox
from tkinter import filedialog
import math
import threading #多线程
import xlwt #写文件
import sys
sys.path.append('..')
import global_manager as gm #全局变量管理器
import operations.comment_judge as cm_judger

class settings():
    def __init__(self,master):
        self.master=master
        self.window=tk.Toplevel()
        self.window.title('设置路径')
        self.window.iconbitmap('华南理工大学logo.ico')
        self.window.protocol('WM_DELETE_WINDOW',self.close_window)
        self.temp_driver_path=gm.get_global('driver_path')
        self.temp_chrome_path=gm.get_global('chrome_path')
        gm.set_global('setting_window_flag',True)
        #driver路径
        temp_text=tk.Label(self.window,text='Google Chrome Driver 路径:',font=('微软雅黑',12,'bold'))
        temp_text.grid(row=0,column=0,pady=5,padx=5)
        self.driver_inputbox=tk.Entry(self.window,text=self.temp_driver_path,width=30)
        self.driver_inputbox.bind('<Return>',self.refresh_driver_path_event)
        self.driver_inputbox.insert(0,gm.get_global('driver_path'))
        self.driver_inputbox.grid(row=0,column=1,pady=5)
        self.driver_button=tk.Button(self.window,text='driver路径选择',font=('华文中宋',14),command=self.driver_select)
        self.driver_button.grid(row=0,column=2,padx=5,pady=5)
        #Chrome路径
        temp_text=tk.Label(self.window,text='Google Chrome.exe 路径:',font=('微软雅黑',12,'bold'))
        temp_text.grid(row=1,column=0,pady=5,padx=5)
        self.chrome_inputbox=tk.Entry(self.window,text=self.temp_chrome_path,width=30)
        self.chrome_inputbox.bind('<Return>',self.refresh_chrome_path_event)
        self.chrome_inputbox.insert(0,gm.get_global('chrome_path'))
        self.chrome_inputbox.grid(row=1,column=1,pady=5)
        self.chrome_button=tk.Button(self.window,text='Chrome路径选择',font=('华文中宋',14),command=self.chrome_select)
        self.chrome_button.grid(row=1,column=2,padx=5,pady=5)
        #确认按钮
        self.confirm_button=tk.Button(self.window,text='确认',font=('华文中宋',14),command=self.confirm)
        self.confirm_button.grid(row=2,column=0,columnspan=3)
        
    def refresh_driver_path_core(self): #真正的driver路径改变函数
        self.temp_driver_path=self.driver_inputbox.get()
    
    def refresh_driver_path_event(self,event): #driver路径改变事件线程
        self.refresh_driver_path_event_threading=threading.Thread(target=self.refresh_driver_path_core)
        self.refresh_driver_path_event_threading.setDaemon(True)
        self.refresh_driver_path_event_threading.start()
    
    def driver_select_core(self): #打开文件选择窗选择文件
        temp_path=filedialog.askopenfilename(title='选择driver文件路径')
        self.window.wm_attributes('-topmost',True)
        self.temp_driver_path=temp_path
        self.driver_inputbox.delete(0,tk.END)
        self.driver_inputbox.insert(tk.END,temp_path)
    
    def driver_select(self): #打开driver路径线程
        self.driver_select_threading=threading.Thread(target=self.driver_select_core)
        self.driver_select_threading.setDaemon(True)
        self.driver_select_threading.start()
        
    def refresh_chrome_path_core(self): #真正的driver路径改变函数
        self.temp_chrome_path=self.chrome_inputbox.get()
    
    def refresh_chrome_path_event(self,event): #chrome路径改变事件线程
        self.refresh_chrome_path_event_threading=threading.Thread(target=self.refresh_chrome_path_core)
        self.refresh_chrome_path_event_threading.setDaemon(True)
        self.refresh_chrome_path_event_threading.start()
    
    def chrome_select_core(self): #打开文件选择窗选择文件
        temp_path=filedialog.askopenfilename(title='选择Chrome.exe文件路径')
        self.window.wm_attributes('-topmost',True)
        self.temp_chrome_path=temp_path
        self.chrome_inputbox.delete(0,tk.END)
        self.chrome_inputbox.insert(tk.END,temp_path)
    
    def chrome_select(self): #打开chrome路径线程
        self.chrome_select_threading=threading.Thread(target=self.chrome_select_core)
        self.chrome_select_threading.setDaemon(True)
        self.chrome_select_threading.start()
    
    def close_window(self):
        gm.set_global('setting_window_flag',False)
        self.window.destroy()
        
    def confirm_core(self): #确认函数核心
        confirm=messagebox.askyesno('确认选择','您是否确认当前路径正确？\n注意:driver版本号要和Chrome版本号对应！')
        if confirm:
            gm.set_global('driver_path',self.temp_driver_path)
            gm.set_global('chrome_path',self.temp_driver_path)
            messagebox.showinfo('选择成功','您已成功完成路径修改！')
            self.close_window()
        else:
            self.window.wm_attributes('-topmost',True)
    
    def confirm(self): #确认线程
        self.confirm_threading=threading.Thread(target=self.confirm_core)
        self.confirm_threading.setDaemon(True)
        self.confirm_threading.start()

def set_thread(master):
    temp=settings(master)
    while gm.get_global('setting_window_flag'):
        pass
    del temp

class comparison_adjust():
    def __init__(self,master):
        self.master=master
        self.window=tk.Toplevel()
        self.window.title('比对项设置')
        self.window.iconbitmap('华南理工大学logo.ico')
        gm.set_global('compare_setting_window_flag',True)
        self.window.protocol('WM_DELETE_WINDOW',self.close_window)
        #本地暂存记录
        self.temp_settings=[]
        for temp in range(17):
            t=tk.IntVar()
            t.set(1)
            self.temp_settings.append(t)
        #查询评论数目调数
        self.comment_num=gm.get_global('comment_number')
        #本窗口大标题
        self.text=tk.Label(self.window,text='酒店查询比对项设置',font=('华文中宋',15,'bold'))
        self.text.grid(row=0,column=0,columnspan=4,sticky=tk.W+tk.E)
        self.section_names=('','评分','好评率','房价','入住时间','离店时间','联系方式',
                            '简介','儿童政策','附加费用','入住须知','网络设施',
                            '停车设施','房间设施','其他设施','酒店服务','评价感情倾向')
        #分别将16个对比项放到窗口上
        self.checkbutton_group=[]
        little_dict={1:0,2:1,3:2,0:3}
        for index in range(1,17):
            temp=tk.Checkbutton(self.window,text=self.section_names[index],variable=self.temp_settings[index],
                                font=('宋体',12))
            put_col=little_dict[index%4]
            put_row=math.ceil(index/4)
            temp.grid(row=put_row,column=put_col,sticky=tk.W+tk.E+tk.N+tk.S)
            self.checkbutton_group.append(temp)
        #抓取评论数框
        self.another_text=tk.Label(self.window,text='抓取评论数量:',font=('宋体',12))
        self.another_text.grid(row=5,column=0,sticky=tk.E+tk.W)
        self.comment_number_spin=tk.Spinbox(self.window,from_=1,to=200,command=self.set_comment_num)
        self.comment_number_spin.delete(0,tk.END)
        self.comment_number_spin.insert(tk.END,str(self.comment_num))
        self.comment_number_spin.grid(row=5,column=1,sticky=tk.W+tk.E+tk.S+tk.N)
        self.comment_number_spin.bind('<Leave>',self.set_comment_num_event)
        self.comment_number_spin.bind('<Return>',self.set_comment_num_event)
        #确认按钮
        self.confirm_button=tk.Button(self.window,text='确认',font=('华文中宋',14,'bold'),command=self.confirm)
        self.confirm_button.grid(row=5,column=2,columnspan=2)
        
    def close_window(self): #关闭窗口
        self.window.destroy()
        gm.set_global('compare_setting_window_flag',False)
        
    def confirm_core(self): #真正的确认函数操作
        confirm=messagebox.askyesno('确认操作','您确认以上设置无误吗？')
        if confirm:
            temp=[]
            for each in self.temp_settings:
                temp.append(each.get())
            temp=tuple(temp)
            gm.set_global('compare_paras',temp)
            gm.set_global('comment_number',self.comment_num)
            self.close_window()
        else:
            self.window.wm_attributes('-topmost',True)
            
    def confirm(self): #确认函数线程
        confirm_threading=threading.Thread(target=self.confirm_core)
        confirm_threading.setDaemon(True)
        confirm_threading.start()
    
    def set_comment_num_core(self): #真正的查询数目更新函数
        try:
            temp=int(self.comment_number_spin.get())
        except:
            messagebox.showerror('输入错误','请输入正整数类型的评论查询数量！')
            self.comment_number_spin.delete(0,tk.END)
            self.comment_number_spin.insert(tk.END,str(self.comment_num))
        else:
            if temp<1:
                messagebox.showerror('输入错误','请输入正的评论查询数量！')
                self.comment_number_spin.delete(0,tk.END)
                self.comment_number_spin.insert(tk.END,str(self.comment_num))
            else:
                self.comment_num=temp
    
    def set_comment_num(self): #查询评论数目更新线程
        self.set_comment_num_threading=threading.Thread(target=self.set_comment_num_core)
        self.set_comment_num_threading.setDaemon(True)
        self.set_comment_num_threading.start()
    
    def set_comment_num_event(self,event): #查询评论数目更新事件线程
        self.set_comment_num_event_threading=threading.Thread(target=self.set_comment_num_core)
        self.set_comment_num_event_threading.setDaemon(True)
        self.set_comment_num_event_threading.start()
    
def comparison_adjust_thread(master):
    temp=comparison_adjust(master)
    while gm.get_global('compare_setting_window_flag'):
        pass
    del temp
    
def outport_thread(master):
    #如果正在比较中或没有比较，则不能导出
    if gm.get_global('detail_progress_window_flag'):
        messagebox.showerror('导出错误','当前正在执行酒店比较操作,无法导出文件！')
        return
    if len(gm.get_global('compared_hotel_list'))==0:
        messagebox.showerror('导出错误','当前还未有比较过的酒店,无法导出文件！')
        return
    file_path=filedialog.asksaveasfilename(title='导出比较表格',filetype=[('03版Excel(*.xls)','.xls')])
    if file_path:
        gm.set_global('outporting',True)
        if not file_path.endswith('.xls'):
            file_path=file_path+'.xls'
        enable_comment=messagebox.askyesno('小提问','您是否需要导出抓取评论？')
        book=xlwt.Workbook()
        sheet=book.add_sheet('酒店比较结果')
        col=0
        row=0
        consult_status=gm.get_global('compare_paras')
        #写入首列
        names=('酒店名','评分','好评率','房价','入住时间','离店时间','联系方式',
               '简介','儿童政策','附加费用','入住须知','网络设施','停车设施',
               '房间设施','其他设施','酒店服务','评价感情倾向')
        for ptr in range(17):
            if consult_status[ptr]:
                sheet.write(row,col,names[ptr])
                row+=1
        if enable_comment:
            sheet.write(row,col,'以下开始为抓取评论')
        #写入内容
        consulted_objects=gm.get_global('compared_hotel_list')
        col=1
        for each in consulted_objects:
            row=0
            hotel_name=each.return_info()[0]
            sheet.write(row,col,hotel_name)
            row+=1
            if consult_status[1]: #比较分数 float
                hotel_score=each.return_info()[1]
                sheet.write(row,col,str(hotel_score))
                row+=1
            if consult_status[2]: #比较好评率 float归一化
                hotel_favor=each.return_info()[2]
                sheet.write(row,col,str(hotel_favor))
                row+=1
            if consult_status[3]: #比较价格 dict
                hotel_price_menu=each.return_info()[3]
                hotel_price=[]
                for room_type in hotel_price_menu.keys():
                    room_price_list=hotel_price_menu[room_type]
                    for price_idx in range(len(room_price_list)):
                        room_price_list[price_idx]=str(room_price_list[price_idx])
                    room_price_str=' '.join(room_price_list)
                    room_type_str=room_type+':'+room_price_str+'    '
                    hotel_price.append(room_type_str)
                hotel_str=''.join(hotel_price)
                sheet.write(row,col,hotel_str)
                row+=1
            if consult_status[4]: #比较最早入住时间 str
                hotel_check_in_time=each.return_info()[4]
                sheet.write(row,col,hotel_check_in_time)
                row+=1
            if consult_status[5]: #比较最晚离店时间 str
                hotel_check_out_time=each.return_info()[5]
                sheet.write(row,col,hotel_check_out_time)
                row+=1
            if consult_status[6]: #比较联系方式 str
                hotel_contact=each.return_info()[6]
                sheet.write(row,col,hotel_contact)
                row+=1
            if consult_status[7]: #比较简介 str
                hotel_intro=each.return_info()[7]
                sheet.write(row,col,hotel_intro)
                row+=1
            if consult_status[8]: #比较儿童政策 list or str
                hotel_children=each.return_info()[8]
                if isinstance(hotel_children,str):
                    hotel_child=hotel_children
                else:
                    hotel_child=';'.join(hotel_children)
                sheet.write(row,col,hotel_child)
                row+=1
            if consult_status[9]: #比较额外费用 str
                hotel_extra=each.return_info()[9]
                sheet.write(row,col,hotel_extra)
                row+=1
            if consult_status[10]: #比较其它须知 str
                hotel_note=each.return_info()[10]
                sheet.write(row,col,hotel_note)
                row+=1
            if consult_status[11]: #比较网络设施 list str
                hotel_net=each.return_info()[11]
                if isinstance(hotel_net,str):
                    pass
                else:
                    if len(hotel_net)==0:
                        hotel_net='未提供'
                    else:
                        hotel_net=';'.join(hotel_net)
                sheet.write(row,col,hotel_net)
                row+=1
            if consult_status[12]: #比较停车设施 list str
                hotel_park=each.return_info()[12]
                if isinstance(hotel_park,str):
                    pass
                else:
                    if len(hotel_park)==0:
                        hotel_park='未提供'
                    else:
                        hotel_park=';'.join(hotel_park)
                sheet.write(row,col,hotel_park)
                row+=1
            if consult_status[13]: #比较房间设施 list
                hotel_rf=each.return_info()[13]
                if len(hotel_rf)==0:
                    hotel_rf='未提供'
                else:
                    hotel_rf=';'.join(hotel_rf)
                sheet.write(row,col,hotel_rf)
                row+=1
            if consult_status[14]: #比较其它设施 list
                hotel_of=each.return_info()[14]
                if len(hotel_of)==0:
                    hotel_of='未提供'
                else:
                    hotel_of=';'.join(hotel_of)
                sheet.write(row,col,hotel_of)
                row+=1
            if consult_status[15]: #比较提供服务 list
                hotel_serve=each.return_info()[15]
                if len(hotel_serve)==0:
                    hotel_serve='未提供'
                else:
                    hotel_serve=';'.join(hotel_serve)
                sheet.write(row,col,hotel_serve)
                row+=1
            if consult_status[16]: #比较评价情感倾向
                temp=cm_judger.comment_judger()
                hotel_comment=each.return_info()[16]
                if len(hotel_comment)==0:
                    hotel_comment='无数据'
                else:
                    positive_cnt,negative_cnt=0,0
                    for each_comment in hotel_comment:
                        category=temp.comment_judge(each_comment['Content'])
                        if category=='积极':
                            positive_cnt+=1
                        else:
                            negative_cnt+=1
                    positive_ratio=100*positive_cnt/(positive_cnt+negative_cnt)
                    hotel_comment='%.2f%%'%positive_ratio
                sheet.write(row,col,hotel_comment)
                row+=1
            if enable_comment:
                comments=each.return_info()[16]
                for each_comment in comments:
                    comment_text=each_comment['Content']
                    sheet.write(row,col,comment_text)
                    row+=1
            col+=1
        try:
            book.save(file_path)
        except Exception as err_info:
            messagebox.showerror('导出错误','导出文件出现错误,错误信息:%s'%err_info)
        else:
            messagebox.showinfo('温馨提示','酒店对比表已经成功导出！')
        finally:
            gm.set_global('outporting',False)