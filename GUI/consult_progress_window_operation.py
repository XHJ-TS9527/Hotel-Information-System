#导入包
import tkinter as tk
from  tkinter.ttk import *
from tkinter import messagebox
import sys
sys.path.append('..')
import global_manager as gm
def open_consult_progress_window():
    def close_consult_progress_bar_window():
        return
    consult_progress_bar_window=tk.Toplevel()
    consult_progress_bar_window.wm_attributes('-topmost',True)
    consult_progress_bar_window.title('查询进度(请勿拖动)')
    consult_progress_bar_window.iconbitmap('华南理工大学logo.ico')
    consult_progress_bar_window.resizable(False,False)
    #consult_progress_bar_window.wm_overrideredirect(True)
    #consult_progress_bar_window.protocol('WM_DELETE_WINDOW',rfb.close_consult_progress_bar_window)
    consult_progress_information=tk.Canvas(consult_progress_bar_window,height=30,width=300)
    consult_progress_text=consult_progress_information.create_text(150,16,text='准备查询...',fill='black',font=('宋体',12,'bold'),anchor=tk.CENTER)
    consult_progress_information.pack()
    consult_progress_bar=Progressbar(consult_progress_bar_window,length=302,mode='determinate',orient=tk.HORIZONTAL)
    consult_progress_bar.pack()
    consult_progress_bar['value']=0
    if gm.get_global('consult_ctrip') and gm.get_global('consult_qunar'):
        consult_progress_bar['maximum']=gm.get_global('total_number')*2
    elif gm.get_global('consult_ctrip'):
        consult_progress_bar['maximum']=gm.get_global('total_number')
    else:
        consult_progress_bar['maximum']=gm.get_global('total_number')
    consult_progress_bar_window.update_idletasks()
    gm.set_global('consult_window',consult_progress_bar_window)
    gm.set_global('consult_bar',consult_progress_bar)
    gm.set_global('consult_info',consult_progress_information)
    gm.set_global('consult_text',consult_progress_text)
def refresh_consult_progress_window():
    consult_progress_bar_window=gm.get_global('consult_window')
    consult_progress_bar=gm.get_global('consult_bar')
    consult_progress_information=gm.get_global('consult_info')
    consult_progress_text=gm.get_global('consult_text')
    if gm.get_global('consult_ctrip') and gm.get_global('consult_qunar'):
        if not gm.get_global('ctrip_complete'):
            temp_ratio=gm.get_global('ctrip_consult_number')/gm.get_global('total_number')*100
            consult_progress_information.itemconfig(consult_progress_text,text='正在查询携程网,进度:%.2f%%'%temp_ratio)
            consult_progress_bar['value']=gm.get_global('ctrip_consult_number')
        else:
            temp_ratio=gm.get_global('qunar_consult_number')/gm.get_global('total_number')*100
            consult_progress_information.itemconfig(consult_progress_text,text='正在查询去哪儿网,进度:%.2f%%'%temp_ratio)
            consult_progress_bar['value']=gm.get_global('qunar_consult_number')+gm.get_global('total_number')
    elif gm.get_global('consult_ctrip'):
        temp_ratio=gm.get_global('ctrip_consult_number')/gm.get_global('total_number')*100
        consult_progress_information.itemconfig(consult_progress_text,text='正在查询携程网,进度:%.2f%%'%temp_ratio)
        consult_progress_bar['value']=gm.get_global('ctrip_consult_number')
    elif gm.get_global('consult_qunar'):
        temp_ratio=gm.get_global('qunar_consult_number')/gm.get_global('total_number')*100
        consult_progress_information.itemconfig(consult_progress_text,text='正在查询去哪儿网,进度:%.2f%%'%temp_ratio)
        consult_progress_bar['value']=gm.get_global('qunar_consult_number')
    consult_progress_bar_window.update_idletasks()
    gm.set_global('consult_window',consult_progress_bar_window)
    gm.set_global('consult_bar',consult_progress_bar)
    gm.set_global('consult_info',consult_progress_information)
    gm.set_global('consult_text',consult_progress_text)
    if consult_progress_bar['value']==consult_progress_bar['maximum']:
        gm.del_global('consult_window')
        consult_progress_bar_window.destroy()
        gm.del_global('consult_bar')
        gm.del_global('consult_info')
        gm.del_global('consult_text')
        messagebox.showinfo('温馨提示','酒店列表查询完成！')