#导入包
    #系统包
import tkinter as tk #GUI
import tkinter.ttk as ttk
from tkinter import messagebox #用于提示
import random #用于随机选择
import threading #多线程
import sys
sys.path.append('..')
import global_manager as gm #全局变量管理器
import exception_classes as excp_cls #自定义异常
    #自定义包
import spiders.crawl_ctrip as ctrip_spider #爬虫类
import spiders.crawl_qunar as qunar_spider
from qunar_city_map_dictionary import * #去哪儿网城市映射
import operations.comment_judge as cm_judger

class consult_hotels(object):
    def __new__(cls,master):
        if not len(gm.get_global('temp_city')):
            messagebox.showerror('查询错误','请选择入住城市！')
            raise excp_cls.consult_hotels_error
        elif not len(gm.get_global('temp_check_in_date')):
            messagebox.showerror('查询错误','请选择入住日期！')
            raise excp_cls.consult_hotels_error
        elif not len(gm.get_global('temp_check_out_date')):
            messagebox.showerror('查询错误','请选择离店日期！')
            raise excp_cls.consult_hotels_error
        elif not len(gm.get_global('temp_destination')):
            messagebox.showerror('查询错误','请输入目的地！')
            raise excp_cls.consult_hotels_error
        else:
            return object.__new__(cls)
    def __init__(self,master):
        self.master=master
        self.window=tk.Toplevel()
        self.window.wm_attributes('-topmost',True)
        self.window.title('酒店列表查询进度')
        self.window.iconbitmap('华南理工大学logo.ico')
        self.window.protocol('WM_DELETE_WINDOW',self.close_window)
        gm.set_global('consult_progress_window_flag',True)
        #读入缓存
        gm.set_global('consult_city',gm.get_global('temp_city'))
        gm.set_global('consult_check_in_date',gm.get_global('temp_check_in_date'))
        gm.set_global('consult_check_out_date',gm.get_global('temp_check_out_date'))
        gm.set_global('consult_destination',gm.get_global('temp_destination'))
        gm.set_global('consult_number',gm.get_global('temp_consult_number'))
        gm.set_global('consult_ctrip',gm.get_global('temp_consult_ctrip'))
        gm.set_global('consult_qunar',gm.get_global('temp_consult_qunar'))
        #构造查询字典
        self.ctrip_consult_dict={'City':gm.get_global('consult_city'),
                            'Check-in Date':gm.get_global('consult_check_in_date'),
                            'Check-out Date':gm.get_global('consult_check_out_date'),
                            'Destination':gm.get_global('consult_destination')}
        self.qunar_consult_dict={'City':qunar_city_map_dict[gm.get_global('consult_city')],
                            'Check-in Date':gm.get_global('consult_check_in_date'),
                            'Check-out Date':gm.get_global('consult_check_out_date'),
                            'Destination':gm.get_global('consult_destination')}
        #进度条上方的文字区域
        self.canvas=tk.Canvas(self.window,height=30,width=300)
        self.canvas_text=self.canvas.create_text(150,16,text='准备查询...',fill='black',font=('宋体',12,'bold'),anchor=tk.CENTER)
        self.canvas.pack()
        #进度条
        self.progress_bar=ttk.Progressbar(self.window,length=302,mode='determinate',orient=tk.HORIZONTAL)
        self.progress_bar.pack()
        self.progress_bar['value']=0
        if gm.get_global('consult_ctrip') and gm.get_global('consult_qunar'):
            self.progress_bar['maximum']=2*gm.get_global('consult_number')
        else:
            self.progress_bar['maximum']=gm.get_global('consult_number')
        self.window.update_idletasks()
        #查询类
        self.ctrip_SPIDER=ctrip_spider.consult_ctrip()
        self.qunar_SPIDER=qunar_spider.consult_qunar()
        self.result_list=[]
    
    def close_window(self):
        gm.set_global('consult_progress_window_flag',False)
        self.window.destroy()
    
    def refresh_window_content(self): #进度条刷新
        while gm.get_global('searching_flag'):
            if gm.get_global('consult_ctrip') and gm.get_global('consult_qunar'):
                total_num=self.ctrip_SPIDER.consulted_number+self.qunar_SPIDER.consulted_number
                self.progress_bar['value']=total_num
                if not self.ctrip_flag:
                    self.canvas.itemconfig(self.canvas_text,text='正在查询携程网,进度:%.2f%%'%(100*total_num/(2*gm.get_global('consult_number'))))
                else:
                    self.canvas.itemconfig(self.canvas_text,text='正在查询去哪儿网,进度:%.2f%%'%(100*total_num/(2*gm.get_global('consult_number'))))
            elif gm.get_global('consult_ctrip'):
                total_num=self.ctrip_SPIDER.consulted_number
                self.progress_bar['value']=total_num
                self.canvas.itemconfig(self.canvas_text,text='正在查询携程网,进度:%.2f%%'%(100*total_num/(2*gm.get_global('consult_number'))))
            else:
                total_num=self.qunar_SPIDER.consulted_number
                self.progress_bar['value']=total_num
                self.canvas.itemconfig(self.canvas_text,text='正在查询去哪儿网,进度:%.2f%%'%(100*total_num/(2*gm.get_global('consult_number'))))
            self.window.update_idletasks()
        self.close_window() #查询完成，关闭窗口
    
    def consult_hotels_information(self): #查询内容
        if gm.get_global('consult_ctrip') and gm.get_global('consult_qunar'):
            try:
                self.ctrip_SPIDER.consult_hotels_core(self.ctrip_consult_dict,gm.get_global('consult_number'))
            except Exception as error_info:
                messagebox.showerror('查询错误','查询出现意外,请联系技术人员。\n您可尝试通过菜单栏中设置选项的重启浏览器内核项解决问题。\n错误信息:%s'%error_info)
                gm.set_global('searching_flag',False)
                return
            result_ctrip=self.ctrip_SPIDER.get_consult_ctrip_list()
            self.ctrip_flag=True
            try:
                self.qunar_SPIDER.consult_hotels_core(self.qunar_consult_dict,gm.get_global('consult_number'))
            except Exception as error_info:
                messagebox.showerror('查询错误','查询出现意外,请联系技术人员。\n您可尝试通过菜单栏中设置选项的重启浏览器内核项解决问题。\n错误信息:%s'%error_info)
                gm.set_global('searching_flag',False)
                return
            result_qunar=self.qunar_SPIDER.get_consult_qunar_list()
            result_ctrip.extend(result_qunar)
            mix_result=result_ctrip
            random.shuffle(mix_result)
            self.result_list=mix_result[0:gm.get_global('consult_number')]
        elif gm.get_global('consult_ctrip'):
            try:
                self.ctrip_SPIDER.consult_hotels_core(self.ctrip_consult_dict,gm.get_global('consult_number'))
            except Exception as error_info:
                messagebox.showerror('查询错误','查询出现意外,请联系技术人员。\n您可尝试通过菜单栏中设置选项的重启浏览器内核项解决问题。\n错误信息:%s'%error_info)
                gm.set_global('searching_flag',False)
                return
            self.result_list=self.ctrip_SPIDER.get_consult_ctrip_list()
        else:
            try:
                self.qunar_SPIDER.consult_hotels_core(self.qunar_consult_dict,gm.get_global('consult_number'))
            except Exception as error_info:
                messagebox.showerror('查询错误','查询出现意外,请联系技术人员。\n您可尝试通过菜单栏中设置选项的重启浏览器内核项解决问题。\n错误信息:%s'%error_info)
                gm.set_global('searching_flag',False)
                return
            self.result_list=self.qunar_SPIDER.get_consult_qunar_list()
        gm.set_global('consulted_hotel_list',self.result_list)
        gm.set_global('consulted_flag',True)
        gm.set_global('searching_flag',False)
        if len(self.result_list)==gm.get_global('consult_number'):
            messagebox.showinfo('温馨提示','酒店列表查询成功！')
        else:
            messagebox.showinfo('温馨提示','酒店列表查询成功！\n该目的地附近房源较少,查不到预定数目酒店！')
    
    def add_history_item_core(self):
        if gm.get_global('consult_ctrip') and gm.get_global('consult_qunar'):
            website_text='携程网|去哪儿网'
        elif gm.get_global('consult_ctrip'):
            website_text='携程网'
        else:
            website_text='去哪儿网'
        history_record='城市:%s,入住日期:%s,离店日期:%s,目的地:%s,查询数量:%d,查询网站:%s'%(gm.get_global('consult_city'),
                        gm.get_global('consult_check_in_date'),gm.get_global('consult_check_out_date'),
                        gm.get_global('consult_destination'),gm.get_global('consult_number'),website_text)
        self.master.consult_history_box.insert(0,history_record)
        self.master.window.update_idletasks()
    
    def run_consult(self): #查询多线程
        gm.set_global('searching_flag',True)
        self.ctrip_flag=False
        self.consult_threading=threading.Thread(target=self.consult_hotels_information)
        self.consult_bar=threading.Thread(target=self.refresh_window_content)
        self.consult_history_threading=threading.Thread(target=self.add_history_item_core)
        self.consult_threading.setDaemon(True)
        self.consult_bar.setDaemon(True)
        self.consult_history_threading.setDaemon(True)
        self.consult_threading.start()
        self.consult_bar.start()
        self.consult_history_threading.start()
    
    def refresh_result_tree_core(self): #刷新主窗结果树函数
        #清空树中全部项目
        old_items=self.master.result_show_tree.get_children()
        [self.master.result_show_tree.delete(item) for item in old_items]
        #加入新查询得到的酒店
        self.master.result_show_tree.tag_configure('evenColor',background='lightpink')
        self.master.result_show_tree.tag_configure('hotelColor',background='lawngreen')
        hotel_cnt=1
        hotel_branch_cnt=1
        for each_hotel in self.result_list:
            each_hotel_info=each_hotel.return_info()
            each_hotel={'Name':each_hotel_info[0],
                        'Address Description':each_hotel_info[1],
                        'Price':each_hotel_info[2],
                        'Score':each_hotel_info[3],
                        'Comment':each_hotel_info[4],
                        'URL':each_hotel_info[5],
                        'Favorable':each_hotel_info[6],
                        'Origin':each_hotel_info[7]}
            tag_hotel_name=self.master.result_show_tree.insert('',tk.END,'hotel_item%i'%hotel_cnt,text=each_hotel['Name'],tag=('hotelColor'))
            hotel_cnt+=1
            row_cnt=1
            for infos in each_hotel.keys():
                if infos=='Address Description':
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
                        self.master.result_show_tree.insert(tag_hotel_name,tk.END,'detail_item%i'%hotel_branch_cnt,
                                                            text=info_Chinese,values=('CNY %s'%each_hotel[infos]))
                    else:
                        self.master.result_show_tree.insert(tag_hotel_name,tk.END,'detail_item%i'%hotel_branch_cnt,
                                                            text=info_Chinese,values=each_hotel[infos])
                else:
                    if infos=='Price':
                        self.master.result_show_tree.insert(tag_hotel_name,tk.END,'detail_item%i'%hotel_branch_cnt,
                                                            text=info_Chinese,values=each_hotel[infos],tags=('evenColor'))
                    else:
                        self.master.result_show_tree.insert(tag_hotel_name,tk.END,'detail_item%i'%hotel_branch_cnt,
                                                            text=info_Chinese,values=each_hotel[infos],tags=('evenColor'))
                hotel_branch_cnt+=1
                row_cnt+=1
            #更新
        self.master.window.update_idletasks()
    
    def refresh_result_tree(self):
        self.refresh_result_tree_threading=threading.Thread(target=self.refresh_result_tree_core)
        self.refresh_result_tree_threading.setDaemon(True)
        self.refresh_result_tree_threading.start()

def consult_hotels_thread(master):
    if gm.get_global('detailing_flag'):
        messagebox.showerror('查询错误','正在进行酒店比较,不能查询！')
        return
    if gm.get_global('consult_progress_window_flag'):
        messagebox.showerror('查询错误','已经在进行酒店清单查询,不用再按了！')
        return
    temp=consult_hotels(master)
    try:
        temp.run_consult()
    except:
        return
    while gm.get_global('searching_flag'):
        pass
    temp.refresh_result_tree()
    del temp
    
class consult_detail_info():
    def __init__(self,master):
        self.master=master
        self.window=tk.Toplevel()
        self.window.title('酒店比较详情查询进度')
        self.window.iconbitmap('华南理工大学logo.ico')
        self.window.protocol('WM_DELETE_WINDOW',self.close_window)
        gm.set_global('detail_progress_window_flag',True)
        #查询清单
        self.consult_objects=gm.get_global('compare_hotel_list')
        #进度条上方的文字区域
        self.canvas=tk.Canvas(self.window,height=30,width=300)
        self.canvas_text=self.canvas.create_text(150,16,text='准备查询...',fill='black',font=('宋体',12,'bold'),anchor=tk.CENTER)
        self.canvas.pack()
        #进度条
        self.progress_bar=ttk.Progressbar(self.window,length=302,mode='determinate',orient=tk.HORIZONTAL)
        self.progress_bar.pack()
        self.progress_bar['value']=0
        self.progress_bar['maximum']=len(self.consult_objects)
        self.window.update_idletasks()
        #爬虫类
        self.ctrip_SPIDER=ctrip_spider.consult_ctrip(True)
        self.qunar_SPIDER=qunar_spider.consult_qunar(True)
        self.consulted_number=0
        self.consulted_result=[]
        #构造查询字典
        self.ctrip_consult_dict={'City':gm.get_global('consult_city'),
                            'Check-in Date':gm.get_global('consult_check_in_date'),
                            'Check-out Date':gm.get_global('consult_check_out_date'),
                            'Destination':gm.get_global('consult_destination')}
        self.qunar_consult_dict={'City':qunar_city_map_dict[gm.get_global('consult_city')],
                            'Check-in Date':gm.get_global('consult_check_in_date'),
                            'Check-out Date':gm.get_global('consult_check_out_date'),
                            'Destination':gm.get_global('consult_destination')}
        
    def refresh_window_content(self): #更新界面信息函数
        while gm.get_global('detailing_flag'):
            self.progress_bar['value']=self.consulted_number
            temp_ratio=100*self.consulted_number/len(self.consult_objects)
            self.canvas.itemconfig(self.canvas_text,text='正在查询,进度:%.2f%%'%temp_ratio)
            self.window.update_idletasks()
        self.close_window()
    
    def consult_detail_information(self):
        self.consulted_result=[]
        for each_target in self.consult_objects:
            origin=each_target.return_info()[7]
            if origin=='携程网':
                try:
                    self.ctrip_SPIDER.consult_single_hotel_ctrip_core(each_target,self.ctrip_consult_dict,gm.get_global('comment_number'))
                except Exception as error_info:
                    messagebox.showerror('查询错误','查询出现错误,请联系技术人员。\n您可尝试通过菜单栏中设置选项的重启浏览器内核项解决问题。\n错误信息:%s'%error_info)
                    gm.set_global('detailing_flag',False)
                    gm.set_global('compared_hotel_list',self.consulted_result)
                    return
                self.consulted_result.append(self.ctrip_SPIDER.this_hotel_detail)
            else:
                try:
                    self.qunar_SPIDER.consult_single_hotel_qunar_core(each_target,self.qunar_consult_dict,gm.get_global('comment_number'))
                except Exception as error_info:
                    messagebox.showerror('查询错误','查询出现错误,请联系技术人员。\n您可尝试通过菜单栏中设置选项的重启浏览器内核项解决问题。\n错误信息:%s'%error_info)
                    gm.set_global('detailing_flag',False)
                    gm.set_global('compared_hotel_list',self.consulted_result)
                    return
                self.consulted_result.append(self.qunar_SPIDER.this_hotel_detail)
            self.consulted_number+=1
        gm.set_global('compared_hotel_list',self.consulted_result)
        gm.set_global('detailing_flag',False)
    
    def run_consult(self):
        gm.set_global('detailing_flag',True)
        self.consult_threading=threading.Thread(target=self.consult_detail_information)
        self.refreshing_threading=threading.Thread(target=self.refresh_window_content)
        self.consult_threading.setDaemon(True)
        self.refreshing_threading.setDaemon(True)
        self.consult_threading.start()
        self.refreshing_threading.start()
    
    def close_window(self):
        self.window.destroy()
        gm.set_global('detail_progress_window_flag',False)
        
class comparison():
    def __init__(self,master):
        self.master=master
        if gm.get_global('compare_window_flag'):
            (gm.get_global('compare_window')).destroy()
        gm.set_global('compare_window_flag',True)
        self.window=tk.Toplevel()
        self.window.title('酒店比较详情')
        self.window.iconbitmap('华南理工大学logo.ico')
        self.window.protocol('WM_DELETE_WINDOW',self.close_window)
        #定义一个frame，把表格放到树里面
        self.frame=tk.Frame(self.window,height=420,width=680)
        self.frame.grid(row=0,column=0)
        #获取评价指标总数
        self.consult_paras=gm.get_global('compare_paras')
        #获取总的酒店详情清单
        self.very_detail_hotel_list=gm.get_global('compared_hotel_list')
        self.hotel_number=len(self.very_detail_hotel_list)
        #定义树
        self.compare_tree=ttk.Treeview(self.frame,columns=('',)*(self.hotel_number+1))
            #标题栏
        self.compare_tree.heading('#0',text='项目')
        for col_index in range(1,self.hotel_number+1):
            this_hotel_name=((self.very_detail_hotel_list[col_index-1]).return_info())[0]
            self.compare_tree.heading('#%d'%col_index,text=this_hotel_name)
        self.compare_tree.pack()
            #旁别的scrollbar
        self.compare_tree_yscrollbar=tk.Scrollbar(self.window,orient=tk.VERTICAL)
        self.compare_tree_yscrollbar.grid(row=0,column=1,sticky=tk.N+tk.S)
        self.compare_tree_yscrollbar.config(command=self.compare_tree.yview)
        self.compare_tree.configure(yscrollcommand=self.compare_tree_yscrollbar.set)
            #底下的scrollbar
        self.compare_tree_xscrollbar=tk.Scrollbar(self.window,orient=tk.HORIZONTAL)
        self.compare_tree_xscrollbar.grid(row=1,column=0,sticky=tk.W+tk.E)
        self.compare_tree_xscrollbar.config(command=self.compare_tree.xview)
        self.compare_tree.configure(xscrollcommand=self.compare_tree_xscrollbar.set)
        #刷新按钮
        self.refresh_button=tk.Button(self.window,text='刷新',font=('华文中宋',14),command=self.refresh_tree)
        self.refresh_button.grid(row=2,column=0,columnspan=2)
        self.window.update_idletasks()
        #如果要加载这个要很久，给个提示
        if self.consult_paras[-1]:
            messagebox.showinfo('温馨提醒','需要对一些评论进行情感分析,这可能需要花费一些时间,请耐心等候。')
            self.window.wm_attributes('-topmost',True)
            self.judger=cm_judger.comment_judger()
            gm.set_global('judger_loaded',True)
            
    def refresh_tree_core(self): #更新树
        #删除旧树
        old_items=self.compare_tree.get_children()
        [self.compare_tree.delete(item) for item in old_items]
        #增加新树
        self.consult_paras=gm.get_global('compare_paras')
        row=1
        self.compare_tree.tag_configure('evenColor',background='aliceblue')
        if self.consult_paras[1]: #比较分数 float
            hotel_scores=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_scores.append(str(each_hotel.return_info()[1]))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='分数',values=hotel_scores)
            else:
                self.compare_tree.insert('',index=tk.END,text='分数',values=hotel_scores,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[2]: #比较好评率 float归一化
            hotel_favors=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_favors.append(str(each_hotel.return_info()[2]))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='好评率',values=hotel_favors)
            else:
                self.compare_tree.insert('',index=tk.END,text='好评率',values=hotel_favors,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[3]: #比较价格 dict
            hotel_prices=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_price_menu=each_hotel.return_info()[3]
                this_hotel_price=[]
                for room_type in this_hotel_price_menu.keys():
                    room_price_list=this_hotel_price_menu[room_type]
                    for price_idx in range(len(room_price_list)):
                        room_price_list[price_idx]=str(room_price_list[price_idx])
                    room_price_str=' '.join(room_price_list)
                    room_type_str=room_type+':'+room_price_str+'    '
                    this_hotel_price.append(room_type_str)
                this_hotel_str=''.join(this_hotel_price)
                hotel_prices.append(this_hotel_str)
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='房价',values=hotel_prices)
            else:
                self.compare_tree.insert('',index=tk.END,text='房价',values=hotel_prices,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[4]: #比较最早入住时间 str
            hotel_check_in_times=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_check_in_times.append(each_hotel.return_info()[4])
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='最早入住时间',values=hotel_check_in_times)
            else:
                self.compare_tree.insert('',index=tk.END,text='最早入住时间',values=hotel_check_in_times,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[5]: #比较最晚离店时间 str
            hotel_check_out_times=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_check_out_times.append(each_hotel.return_info()[5])
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='最晚离店时间',values=hotel_check_out_times)
            else:
                self.compare_tree.insert('',index=tk.END,text='最晚离店时间',values=hotel_check_out_times,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[6]: #比较联系方式 str
            hotel_contacts=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_contacts.append(each_hotel.return_info()[6])
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='联系方式',values=hotel_contacts)
            else:
                self.compare_tree.insert('',index=tk.END,text='联系方式',values=hotel_contacts,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[7]: #比较简介 str
            hotel_intros=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_intros.append(each_hotel.return_info()[7])
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='简介',values=hotel_intros)
            else:
                self.compare_tree.insert('',index=tk.END,text='简介',values=hotel_intros,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[8]: #比较儿童政策 list or str
            hotel_childs=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_children=each_hotel.return_info()[8]
                if isinstance(this_hotel_children,str):
                    hotel_childs.append(this_hotel_children)
                else:
                    hotel_childs.append(';'.join(this_hotel_children))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='儿童政策',values=hotel_childs)
            else:
                self.compare_tree.insert('',index=tk.END,text='儿童政策',values=hotel_childs,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[9]: #比较额外费用 str
            hotel_extras=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_extras.append(each_hotel.return_info()[9])
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='额外费用',values=hotel_extras)
            else:
                self.compare_tree.insert('',index=tk.END,text='额外费用',values=hotel_extras,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[10]: #比较其它须知 str
            hotel_notes=[]
            for each_hotel in self.very_detail_hotel_list:
                hotel_notes.append(each_hotel.return_info()[10])
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='预定须知',values=hotel_notes)
            else:
                self.compare_tree.insert('',index=tk.END,text='预定须知',values=hotel_notes,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[11]: #比较网络设施 list str
            hotel_nets=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_net=each_hotel.return_info()[11]
                if isinstance(this_hotel_net,str):
                    hotel_nets.append(this_hotel_net)
                else:
                    if len(this_hotel_net)==0:
                        hotel_nets.append('未提供')
                    else:
                        hotel_nets.append(';'.join(this_hotel_net))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='网络设施',values=hotel_nets)
            else:
                self.compare_tree.insert('',index=tk.END,text='网络设施',values=hotel_nets,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[12]: #比较停车设施 list str
            hotel_parks=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_park=each_hotel.return_info()[12]
                if isinstance(this_hotel_park,str):
                    hotel_parks.append(this_hotel_park)
                else:
                    if len(this_hotel_park)==0:
                        hotel_parks.append('未提供')
                    else:
                        hotel_parks.append(';'.join(this_hotel_park))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='停车设施',values=hotel_parks)
            else:
                self.compare_tree.insert('',index=tk.END,text='停车设施',values=hotel_parks,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[13]: #比较房间设施 list
            hotel_rfs=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_rf=each_hotel.return_info()[13]
                if len(this_hotel_rf)==0:
                    hotel_rfs.append('未提供')
                else:
                    hotel_rfs.append(';'.join(this_hotel_rf))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='房间设施',values=hotel_rfs)
            else:
                self.compare_tree.insert('',index=tk.END,text='房间设施',values=hotel_rfs,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[14]: #比较其它设施 list
            hotel_ofs=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_of=each_hotel.return_info()[14]
                if len(this_hotel_of)==0:
                    hotel_ofs.append('未提供')
                else:
                    hotel_ofs.append(';'.join(this_hotel_of))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='其它设施',values=hotel_ofs)
            else:
                self.compare_tree.insert('',index=tk.END,text='其它设施',values=hotel_ofs,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[15]: #比较提供服务 list
            hotel_serves=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_serve=each_hotel.return_info()[15]
                if len(this_hotel_serve)==0:
                    hotel_serves.append('未提供')
                else:
                    hotel_serves.append(';'.join(this_hotel_serve))
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='提供服务',values=hotel_serves)
            else:
                self.compare_tree.insert('',index=tk.END,text='提供服务',values=hotel_serves,
                                         tags=('evenColor'))
            row+=1
        if self.consult_paras[16]: #比较评价情感倾向
            if not gm.get_global('judger_loaded'):
                self.judger=cm_judger.comment_judger()
                gm.set_global('judger_loaded',True)
            hotel_comments=[]
            for each_hotel in self.very_detail_hotel_list:
                this_hotel_comment=each_hotel.return_info()[16]
                if len(this_hotel_comment)==0:
                    hotel_comments.append('无数据')
                else:
                    positive_cnt,negative_cnt=0,0
                    for each_comment in this_hotel_comment:
                        category=self.judger.comment_judge(each_comment['Content'])
                        if category=='积极':
                            positive_cnt+=1
                        else:
                            negative_cnt+=1
                    positive_ratio=100*positive_cnt/(positive_cnt+negative_cnt)
                    hotel_comments.append('%.2f%%'%positive_ratio)
            if row%2:
                self.compare_tree.insert('',index=tk.END,text='抓取评论积极倾向',values=hotel_comments)
            else:
                self.compare_tree.insert('',index=tk.END,text='抓取评论积极倾向',values=hotel_comments,
                                         tags=('evenColor'))
        self.window.update_idletasks()
        
    def refresh_tree(self): #更新树的线程
        self.refresh_tree_threading=threading.Thread(target=self.refresh_tree_core)
        self.refresh_tree_threading.setDaemon(False)
        self.refresh_tree_threading.start()

    def close_window(self):
        gm.set_global('compare_window_flag',False)
        self.window.destroy()

def consult_detail_info_thread(master):
    if gm.get_global('searching_flag'):
        messagebox.showerror('比较错误','正在进行酒店清单查询,不能比较！')
        return
    if gm.get_global('detail_progress_window_flag'):
        messagebox.showerror('比较错误','正在进行酒店比较,不用再按了！')
        return
    tree_children_items=master.result_show_tree.get_children()
    if not len(tree_children_items):
        messagebox.showerror('比较错误','还未查询酒店清单,不能比较！')
        return
    if gm.get_global('outporting'):
        messagebox.showerror('比较错误','正在进行导出操作,不能进行比较！')
        return
    selected_item=master.result_show_tree.selection()
    if len(selected_item)==0:
        messagebox.showerror('选择错误','请至少选择一家酒店进行比较！')
        return
    selected_index=[]
    for each in selected_item:
        if 'detail' in each:
            messagebox.showerror('选择错误','请不要选择非酒店名称的项目！')
            return
        selected_index.append(int(each.replace('hotel_item',''))-1)
    compare_hotel_items=[]
    for each_index in selected_index:
        compare_hotel_items.append(gm.get_global('consulted_hotel_list')[int(each_index)])
    gm.set_global('compare_hotel_list',compare_hotel_items)
    temp=consult_detail_info(master)
    temp.run_consult()
    while gm.get_global('detailing_flag'):
        pass
    if len(gm.get_global('compared_hotel_list'))==0:
        return
    temp=comparison(master)
    temp.refresh_tree()
    while gm.get_global('compare_window_flag'):
        pass
    del temp