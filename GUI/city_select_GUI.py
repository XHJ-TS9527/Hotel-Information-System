#导入包
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Notebook,Treeview
import sys
sys.path.append('..')
import global_manager as gm

def city_selection(canvas,city_sel_text,main_window):
    temp_city=''
    #一些回调函数定义
    def close_window():
        gm.set_global('city_window',0)
        city_selection_window.destroy()
    def tree_select(event):
        global temp_city
        target_widget=event.widget
        target_item=target_widget.selection()[0]
        temp_city=target_widget.item(target_item,'text')
    def confirm_selection(canvas,city_sel_text,main_window):
        global temp_city
        if temp_city in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            messagebox.showerror('城市选择错误','请选择一个城市名称！')
            city_selection_window.wm_attributes('-topmost',True)
            return
        confirm=messagebox.askyesno('确认选择城市','是否确定目标城市为：%s？'%temp_city)
        if confirm:
            gm.set_global('city_text',temp_city)
            gm.set_global('city_window',0)
            city_selection_window.destroy()
            canvas.itemconfig(city_sel_text,text='入住城市:%s'%temp_city)
            main_window.update_idletasks()
        else:
            city_selection_window.wm_attributes('-topmost',True)
    #检查是否已经打开选择窗口
    if gm.get_global('city_window'):
        return
    #打开新窗口
    city_selection_window=tk.Toplevel()
    city_selection_window.iconbitmap('华南理工大学logo.ico')
    city_selection_window.title('入住城市选择')
    city_select_notebook=Notebook(city_selection_window)
    gm.set_global('city_window',1)
    city_selection_window.protocol('WM_DELETE_WINDOW',close_window)
    #加Frame
    frame1=tk.Frame(city_select_notebook)
    frame2=tk.Frame(city_select_notebook)
    frame3=tk.Frame(city_select_notebook)
    frame4=tk.Frame(city_select_notebook)
    frame5=tk.Frame(city_select_notebook)
    #写入城市清单-Frame1
    A=['阿坝','安吉县','安顺','鞍山','安庆','安康','阿尔山市','安阳','阿勒泰','阿拉善盟']
    B=['北京','北海','本溪','保定','宝鸡','保亭','白山','包头','蚌埠','布尔津县','博鳌','保山','博罗县','白色']
    C=['成都','重庆','长沙','常州','长春','长白山 白山','常德','郴州','赤峰','赤水市','湖州']
    D=['大理','大连','丹东','稻城县','东莞','敦煌市','大同','都江堰市','迪庆','东营','丹霞山']
    E=['峨眉山市','额济纳旗','恩施自治州','鄂尔多斯','恩施市','恩平市']
    tree1=Treeview(frame1,selectmode=tk.BROWSE)
    tree1scrollbar=tk.Scrollbar(frame1)
    tree1.tag_configure('evenColor',background='lightblue')
    tree1.heading('#0',text='城市')
    idA=tree1.insert('',index=tk.END,text='A')
    idB=tree1.insert('',index=tk.END,text='B')
    idC=tree1.insert('',index=tk.END,text='C')
    idD=tree1.insert('',index=tk.END,text='D')
    idE=tree1.insert('',index=tk.END,text='E')
    row=1
    for city in A:
        if row%2:
            tree1.insert(idA,index=tk.END,text=city)
        else:
            tree1.insert(idA,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in B:
        if row%2:
            tree1.insert(idB,index=tk.END,text=city)
        else:
            tree1.insert(idB,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in C:
        if row%2:
            tree1.insert(idC,index=tk.END,text=city)
        else:
            tree1.insert(idC,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in D:
        if row%2:
            tree1.insert(idD,index=tk.END,text=city)
        else:
            tree1.insert(idD,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in E:
        if row%2:
            tree1.insert(idE,index=tk.END,text=city)
        else:
            tree1.insert(idE,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    tree1.bind('<<TreeviewSelect>>',tree_select)
    tree1.pack(side=tk.LEFT,fill=tk.Y)
    tree1scrollbar.pack(side=tk.LEFT,fill=tk.Y)
    tree1scrollbar.config(command=tree1.yview)
    tree1.configure(yscrollcommand=tree1scrollbar.set)
    #写入城市清单-Frame2
    F=['凤凰县','福州','佛山','防城港','抚仙湖','凤城市','阜阳','抚顺','佛冈县']
    G=['广州','桂林','贵阳','甘孜','广元','赣州','广安']
    H=['杭州','黄山','惠州','哈尔滨','海口','合肥','湖州','呼和浩特','横店','惠东县','河源']
    J=['济南','九寨沟县','嘉兴','九江','江门','金华','锦州','吉林','景德镇','嘉峪关','焦作','晋中','九华山','嘉善县']
    tree2=Treeview(frame2,selectmode=tk.BROWSE)
    tree2scrollbar=tk.Scrollbar(frame2)
    tree2.tag_configure('evenColor',background='lightgreen')
    tree2.heading('#0',text='城市')
    idF=tree2.insert('',index=tk.END,text='F')
    idG=tree2.insert('',index=tk.END,text='G')
    idH=tree2.insert('',index=tk.END,text='H')
    idJ=tree2.insert('',index=tk.END,text='J')
    row=1
    for city in F:
        if row%2:
            tree2.insert(idF,index=tk.END,text=city)
        else:
            tree2.insert(idF,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in G:
        if row%2:
            tree2.insert(idG,index=tk.END,text=city)
        else:
            tree2.insert(idG,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in H:
        if row%2:
            tree2.insert(idH,index=tk.END,text=city)
        else:
            tree2.insert(idH,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in J:
        if row%2:
            tree2.insert(idJ,index=tk.END,text=city)
        else:
            tree2.insert(idJ,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    tree2.bind('<<TreeviewSelect>>',tree_select)
    tree2.pack(side=tk.LEFT,fill=tk.Y)
    tree2scrollbar.pack(side=tk.LEFT,fill=tk.Y)
    tree2scrollbar.config(command=tree2.yview)
    tree2.configure(yscrollcommand=tree2scrollbar.set)
    #写入城市清单-Frame3
    K=['昆明','开封','康定市','昆山市','凯里市','克什克腾旗','喀纳斯','宽甸','开平市']
    L=['丽江','洛阳','兰州','拉萨','乐山','阆中市','荔波湾','柳州','丽水','理县','临沂','陵水','临安区']
    M=['莫干山','绵阳','梅州','茂名','弥勒县','牡丹江','眉山','茂县']
    N=['南京','宁波','南宁','南昌','南通','南充','南昆山','南平','南阳','南澳岛','宁德','内江']
    P=['平遥县','盘锦','蓬莱市','莆田','平潭县','攀枝花','萍乡','普洱','普者黑']
    tree3=Treeview(frame3,selectmode=tk.BROWSE)
    tree3scrollbar=tk.Scrollbar(frame3)
    tree3.tag_configure('evenColor',background='lightpink')
    tree3.heading('#0',text='城市')
    idK=tree3.insert('',index=tk.END,text='K')
    idL=tree3.insert('',index=tk.END,text='L')
    idM=tree3.insert('',index=tk.END,text='M')
    idN=tree3.insert('',index=tk.END,text='N')
    idP=tree3.insert('',index=tk.END,text='P')
    row=1
    for city in K:
        if row%2:
            tree3.insert(idK,index=tk.END,text=city)
        else:
            tree3.insert(idK,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in L:
        if row%2:
            tree3.insert(idL,index=tk.END,text=city)
        else:
            tree3.insert(idL,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in M:
        if row%2:
            tree3.insert(idM,index=tk.END,text=city)
        else:
            tree3.insert(idM,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in N:
        if row%2:
            tree3.insert(idN,index=tk.END,text=city)
        else:
            tree3.insert(idN,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in P:
        if row%2:
            tree3.insert(idP,index=tk.END,text=city)
        else:
            tree3.insert(idP,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    tree3.bind('<<TreeviewSelect>>',tree_select)
    tree3.pack(side=tk.LEFT,fill=tk.Y)
    tree3scrollbar.pack(side=tk.LEFT,fill=tk.Y)
    tree3scrollbar.config(command=tree3.yview)
    tree3.configure(yscrollcommand=tree3scrollbar.set)
    #写入城市清单-Frame4
    Q=['青岛','秦皇岛','千湖岛','清远','泉州','琼海','黔东南','曲阜市','青城山','衢州','钦州']
    R=['日照','若尔盖县','荣成市','瑞丽市','乳山市','乳源','仁化县','四姑娘山镇','日喀则','仁寿县']
    S=['上海','三亚','深圳','苏州','沈阳','绍兴','石家庄','韶关','汕头','神农架','三清山','嵊泗县','十堰']
    T=['天津','太原','秦安','腾冲市','台山市','天水','台州','唐山','桐庐县','泰州','同里','铜仁']
    W=['武汉','乌镇','无锡','威海','乌鲁木齐','温州','武夷山市','武隆区','婺源县','芜湖','潍坊','五台山','武当山','文昌']
    tree4=Treeview(frame4,selectmode=tk.BROWSE)
    tree4scrollbar=tk.Scrollbar(frame4)
    tree4.tag_configure('evenColor',background='lightsalmon')
    tree4.heading('#0',text='城市')
    idQ=tree4.insert('',index=tk.END,text='Q')
    idR=tree4.insert('',index=tk.END,text='R')
    idS=tree4.insert('',index=tk.END,text='S')
    idT=tree4.insert('',index=tk.END,text='T')
    idW=tree4.insert('',index=tk.END,text='W')
    row=1
    for city in Q:
        if row%2:
            tree4.insert(idQ,index=tk.END,text=city)
        else:
            tree4.insert(idQ,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in R:
        if row%2:
            tree4.insert(idR,index=tk.END,text=city)
        else:
            tree4.insert(idR,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in S:
        if row%2:
            tree4.insert(idS,index=tk.END,text=city)
        else:
            tree4.insert(idS,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in T:
        if row%2:
            tree4.insert(idT,index=tk.END,text=city)
        else:
            tree4.insert(idT,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in W:
        if row%2:
            tree4.insert(idW,index=tk.END,text=city)
        else:
            tree4.insert(idW,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    tree4.bind('<<TreeviewSelect>>',tree_select)
    tree4.pack(side=tk.LEFT,fill=tk.Y)
    tree4scrollbar.pack(side=tk.LEFT,fill=tk.Y)
    tree4scrollbar.config(command=tree4.yview)
    tree4.configure(yscrollcommand=tree4scrollbar.set)
    #写入城市清单-Frame5
    X=['厦门','西安','西塘镇','西昌市','西宁','西双版纳','香格里拉县','巽寮湾','徐州','西江千户苗寨','兴城市','新都桥','襄阳','湘西','咸阳']
    Y=['阳朔县','扬州','阳江','烟台','银川','宜昌','延吉市','义乌市','雅安','延安','宜宾','营口','云台山','宜兴市']
    Z=['珠海','张家界','郑州','舟山','镇远县','肇庆','中山','湛江','漳州','镇江','周庄','中卫','张掖','张家口','遵义']
    tree5=Treeview(frame5,selectmode=tk.BROWSE)
    tree5scrollbar=tk.Scrollbar(frame5)
    tree5.tag_configure('evenColor',background='lightseagreen')
    tree5.heading('#0',text='城市')
    idX=tree5.insert('',index=tk.END,text='X')
    idY=tree5.insert('',index=tk.END,text='Y')
    idZ=tree5.insert('',index=tk.END,text='Z')
    row=1
    for city in X:
        if row%2:
            tree5.insert(idX,index=tk.END,text=city)
        else:
            tree5.insert(idX,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in Y:
        if row%2:
            tree5.insert(idY,index=tk.END,text=city)
        else:
            tree5.insert(idY,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    row=1
    for city in Z:
        if row%2:
            tree5.insert(idZ,index=tk.END,text=city)
        else:
            tree5.insert(idZ,index=tk.END,text=city,tags=('evenColor'))
        row+=1
    tree5.bind('<<TreeviewSelect>>',tree_select)
    tree5.pack(side=tk.LEFT,fill=tk.Y)
    tree5scrollbar.pack(side=tk.LEFT,fill=tk.Y)
    tree5scrollbar.config(command=tree5.yview)
    tree5.configure(yscrollcommand=tree5scrollbar.set)
    #将Frame加入窗体
    city_select_notebook.add(frame1,text='ABCDE')
    city_select_notebook.add(frame2,text='FGHJ')
    city_select_notebook.add(frame3,text='KLMNP')
    city_select_notebook.add(frame4,text='QRSTW')
    city_select_notebook.add(frame5,text='XYZ')
    city_select_notebook.pack(side=tk.TOP)
    #确定按钮
    confirm_button=tk.Button(city_selection_window,text='确认',font=('华文中宋',14),command=lambda:confirm_selection(canvas,city_sel_text,main_window))
    confirm_button.pack(side=tk.BOTTOM)