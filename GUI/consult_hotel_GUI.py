#导入包
import tkinter as tk
from tkinter import messagebox
import sys
import random
sys.path.append('..')
import global_manager as gm
import 爬虫.crawl_ctrip as ctrip_crawl_mod
import 爬虫.crawl_qunar as qunar_crawl_mod
import 爬虫.simulation_explorer_driver as sim_driver
import consult_progress_window_operation as cpwo
def consult_hotels(destination_text):
    #打开一个新窗口
    cpwo.open_consult_progress_window()
    #打开浏览器
    driver_exe_path=r'C:\Users\SCUTEEXHJ\Desktop\应用程序\chromedriver61.exe'
    chrome_exe_path=r'C:\Program Files\Google\Chrome\App\Google Chrome\chrome.exe'
    if not gm.get_global('ctrip_open_flag'):
        ctrip_driver=sim_driver.start_explorer_driver(driver_exe_path,chrome_exe_path)
        gm.set_global('ctrip_driver',ctrip_driver)
        gm.set_global('ctrip_open_flag',True)
    else:
        ctrip_driver=gm.get_global('ctrip_driver')
    if not gm.get_global('qunar_open_flag'):
        qunar_driver=sim_driver.start_explorer_driver(driver_exe_path,chrome_exe_path)
        gm.set_global('qunar_driver',qunar_driver)
        gm.set_global('qunar_open_flag',True)
    else:
        qunar_driver=gm.get_global('qunar_driver')
    #生成查询字典
    ctrip_consult_dict=dict()
    qunar_consult_dict=dict()
        #城市
    city_text=gm.get_global('city_text')
    if city_text=='请选择':
        messagebox.showerror('查询出错啦！','请选择入住城市！')
        return
    ctrip_consult_dict['City']=city_text
            #去哪儿拼音城市映射
    file=open('D:\学习与工作\学习\学校的课\大三上\Python程序语言基础\大作业\代码\爬虫\去哪儿城市拼音映射表.csv','rt')
    map_list=file.readlines()
    file.close()
    for each_city in map_list:
        tmp_city=each_city.split(',')
        if city_text==tmp_city[0]:
            qunar_city_text=tmp_city[1].replace('\n','')
            break
    qunar_consult_dict['City']=qunar_city_text
        #目的地
    if not len(destination_text):
        messagebox.showerror('查询出错啦！','请输入目的地！')
        return
    gm.set_global('destination_text',destination_text)
    ctrip_consult_dict['Destination']=destination_text
    qunar_consult_dict['Destination']=destination_text
        #入住日期
    check_in_date_text=gm.get_global('check_in_date_text')
    if check_in_date_text=='请选择':
        messagebox.showerror('查询出错啦！','请选择入住日期！')
        return
    ctrip_consult_dict['Check-in Date']=check_in_date_text
    qunar_consult_dict['Check-in Date']=check_in_date_text
        #离店日期
    check_out_date_text=gm.get_global('check_out_date_text')
    if check_out_date_text=='请选择':
        messagebox.showerror('查询出错啦！','请选择离店日期！')
        return
    ctrip_consult_dict['Check-out Date']=check_out_date_text
    qunar_consult_dict['Check-out Date']=check_out_date_text
    gm.set_global('ctrip_consult_number',0)
    gm.set_global('qunar_consult_number',0)
    #查询酒店
    if gm.get_global('consult_ctrip') and gm.get_global('consult_qunar'):
        gm.set_global('ctrip_complete',False)
        ctrip_hotels,ctrip_driver=ctrip_crawl_mod.consult_hotels_ctrip(gm.get_global('ctrip_driver'),ctrip_consult_dict,gm.get_global('total_number'))
        gm.set_global('ctrip_complete',True)
        qunar_hotels,qunar_driver=qunar_crawl_mod.consult_hotels_qunar(gm.get_global('qunar_driver'),qunar_consult_dict,gm.get_global('total_number'))
        gm.set_global('ctrip_driver',ctrip_driver)
        gm.set_global('qunar_driver',qunar_driver)
        gm.del_global('ctrip_complete')
        ctrip_hotels.extend(qunar_hotels)
        mix_hotels=ctrip_hotels
    elif gm.get_global('consult_ctrip'):
        mix_hotels,ctrip_driver=ctrip_crawl_mod.consult_hotels_ctrip(gm.get_global('ctrip_driver'),ctrip_consult_dict,gm.get_global('total_number'))
        gm.set_global('ctrip_driver',ctrip_driver)
    else:
        mix_hotels,qunar_driver=qunar_crawl_mod.consult_hotels_qunar(gm.get_global('qunar_driver'),qunar_consult_dict,gm.get_global('total_number'))
        gm.set_global('qunar_driver',qunar_driver)
    random.shuffle(mix_hotels)
    shown_hotels=mix_hotels[0:gm.get_global('total_number')]
    gm.set_global('consulted_hotels',shown_hotels)