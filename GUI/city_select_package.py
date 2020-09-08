#导入包
    #系统包
import tkinter as tk #GUI
import tkinter.ttk as ttk
from tkinter import messagebox #用于提示
import threading #多线程
import sys
sys.path.append('..')
import global_manager as gm #全局变量管理器

class city_tree():
    def __init__(self,tree_frame,tree_labels,tree_values,tree_color):
        #初始化格式
        self.tree=ttk.Treeview(tree_frame,selectmode=tk.BROWSE)
        self.treescrollbar=tk.Scrollbar(tree_frame)
        self.tree.tag_configure('evenColor',background=tree_color)
        self.tree.heading('#0',text='城市')
        #写入表
        for group_index in range(len(tree_labels)):
            tree_id=self.tree.insert('',index=tk.END,text=tree_labels[group_index])
            tree_label_city=tree_values[group_index]
            row=0
            for city in tree_label_city:
                if row%2:
                    self.tree.insert(tree_id,index=tk.END,text=city)
                else:
                    self.tree.insert(tree_id,index=tk.END,text=city,tags=('evenColor'))
                row+=1
        #放置这些元件
        self.tree.bind('<<TreeviewSelect>>',self.tree_select)
        self.tree.pack(side=tk.LEFT,fill=tk.Y)
        self.treescrollbar.pack(side=tk.LEFT,fill=tk.Y)
        #元件联结
        self.treescrollbar.config(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treescrollbar.set)
    
    def tree_select_core(self,*args): #真正的树选中后的触发事件
        event=args[0]
        target_widget=event.widget
        target_item=target_widget.selection()[0]
        gm.set_global('temp_city',target_widget.item(target_item,'text'))
    
    def tree_select(self,event): #树选中线程
        self.tree_select_threading=threading.Thread(target=self.tree_select_core,args=(event,))
        self.tree_select_threading.setDaemon(True)
        self.tree_select_threading.start()

class city_select():
    def __init__(self,master):
        self.master=master
        #打开新窗口
        self.window=tk.Toplevel()
        self.window.iconbitmap('华南理工大学logo.ico')
        self.window.title('入住城市选择')
        self.notebook=ttk.Notebook(self.window)
        gm.set_global('city_select_window_flag',True)
        self.window.protocol('WM_DELETE_WINDOW',self.close_city_selection_window)
        #加Frame
        for frame_index in range(5):
            temp_frame=tk.Frame(self.notebook)
            if frame_index==0:
                frame_labels=('A','B','C','D','E')
                frame_color='lightblue'
                A=('阿坝','安吉县','安顺','鞍山','安庆','安康','阿尔山市','安阳','阿勒泰','阿拉善盟')
                B=('北京','北海','本溪','保定','宝鸡','保亭','白山','包头','蚌埠','布尔津县','博鳌','保山','博罗县','白色')
                C=('成都','重庆','长沙','常州','长春','长白山 白山','常德','郴州','赤峰','赤水市','湖州')
                D=('大理','大连','丹东','稻城县','东莞','敦煌市','大同','都江堰市','迪庆','东营','丹霞山')
                E=('峨眉山市','额济纳旗','恩施自治州','鄂尔多斯','恩施市','恩平市')
                frame_values=(A,B,C,D,E)
            elif frame_index==1:
                frame_labels=('F','G','H','J')
                frame_color='lightgreen'
                F=('凤凰县','福州','佛山','防城港','抚仙湖','凤城市','阜阳','抚顺','佛冈县')
                G=('广州','桂林','贵阳','甘孜','广元','赣州','广安')
                H=('杭州','黄山','惠州','哈尔滨','海口','合肥','湖州','呼和浩特','横店','惠东县','河源')
                J=('济南','九寨沟县','嘉兴','九江','江门','金华','锦州','吉林','景德镇','嘉峪关','焦作','晋中','九华山','嘉善县')
                frame_values=(F,G,H,J)
            elif frame_index==2:
                frame_labels=('K','L','M','N','P')
                frame_color='lightpink'
                K=('昆明','开封','康定市','昆山市','凯里市','克什克腾旗','喀纳斯','宽甸','开平市')
                L=('丽江','洛阳','兰州','拉萨','乐山','阆中市','荔波湾','柳州','丽水','理县','临沂','陵水','临安区')
                M=('莫干山','绵阳','梅州','茂名','弥勒县','牡丹江','眉山','茂县')
                N=('南京','宁波','南宁','南昌','南通','南充','南昆山','南平','南阳','南澳岛','宁德','内江')
                P=('平遥县','盘锦','蓬莱市','莆田','平潭县','攀枝花','萍乡','普洱','普者黑')
                frame_values=(K,L,M,N,P)
            elif frame_index==3:
                frame_labels=('Q','R','S','T','W')
                frame_color='lightsalmon'
                Q=('青岛','秦皇岛','千湖岛','清远','泉州','琼海','黔东南','曲阜市','青城山','衢州','钦州')
                R=('日照','若尔盖县','荣成市','瑞丽市','乳山市','乳源','仁化县','四姑娘山镇','日喀则','仁寿县')
                S=('上海','三亚','深圳','苏州','沈阳','绍兴','石家庄','韶关','汕头','神农架','三清山','嵊泗县','十堰')
                T=('天津','太原','秦安','腾冲市','台山市','天水','台州','唐山','桐庐县','泰州','同里','铜仁')
                W=('武汉','乌镇','无锡','威海','乌鲁木齐','温州','武夷山市','武隆区','婺源县','芜湖','潍坊','五台山','武当山','文昌')
                frame_values=(Q,R,S,T,W)
            else:
                frame_labels=('X','Y','Z')
                frame_color='lightseagreen'
                X=('厦门','西安','西塘镇','西昌市','西宁','西双版纳','香格里拉县','巽寮湾','徐州','西江千户苗寨','兴城市','新都桥','襄阳','湘西','咸阳')
                Y=('阳朔县','扬州','阳江','烟台','银川','宜昌','延吉市','义乌市','雅安','延安','宜宾','营口','云台山','宜兴市')
                Z=('珠海','张家界','郑州','舟山','镇远县','肇庆','中山','湛江','漳州','镇江','周庄','中卫','张掖','张家口','遵义')
                frame_values=(X,Y,Z)
            frame_tree=city_tree(temp_frame,frame_labels,frame_values,frame_color)
            self.notebook.add(temp_frame,text=''.join(frame_labels))
        self.notebook.pack(side=tk.TOP)
        #加确定按钮
        self.confirm_button=tk.Button(self.window,text='确认',font=('华文中宋',14),command=self.confirm)
        self.confirm_button.pack(side=tk.BOTTOM)
        
    def close_city_selection_window(self):
        gm.set_global('city_select_window_flag',False)
        self.window.destroy()

    def confirm_core(self): #确认选择
        if gm.get_global('temp_city') in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            messagebox.showerror('选择错误','请选择一个城市名称！')
            self.window.wm_attributes('-topmost',True)
            return
        elif gm.get_global('temp_city')=='请选择':
            messagebox.showerror('选择错误','请选择一个城市名称！')
            self.window.wm_attributes('-topmost',True)
            return
        temp_confirm=messagebox.askyesno('确认选择','是否确定目标城市为：%s？'%gm.get_global('temp_city'))
        if temp_confirm:
            self.close_city_selection_window()
            self.master.canvas.itemconfig(self.master.city_text,text='入住城市:%s'%gm.get_global('temp_city'))
            self.master.window.update_idletasks()
        else:
            self.window.wm_attributes('-topmost',True)
    
    def confirm(self): #确认选择线程
        self.confirm_threading=threading.Thread(target=self.confirm_core)
        self.confirm_threading.setDaemon(True)
        self.confirm_threading.start()

def city_select_thread(master):
    if not gm.get_global('city_select_window_flag'):
        temp=city_select(master)
        while gm.get_global('city_select_window_flag'):
            pass
        del temp