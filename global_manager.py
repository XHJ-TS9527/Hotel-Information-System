def initial_global_dict(): #初始化全局变量管理字典
    global global_dict
    global_dict=dict()
    #窗口管理
    global_dict['setting_window_flag']=False #设置窗管理
    global_dict['city_select_window_flag']=False #城市选择窗
    global_dict['check_in_calendar_window_flag']=False #入住日期选择窗
    global_dict['check_out_calendar_window_flag']=False #离店日期选择窗 
    global_dict['consult_progress_window_flag']=False #查询概要进度窗
    global_dict['detail_progress_window_flag']=False #查询详情进度窗
    global_dict['compare_window_flag']=False #比较详情窗
    global_dict['compare_setting_window_flag']=False #比较项设置窗
    #标志位管理
    global_dict['consult_ctrip']=True #要查询携程
    global_dict['temp_consult_ctrip']=True
    global_dict['consult_qunar']=True #要查询去哪儿
    global_dict['temp_consult_qunar']=True
    global_dict['ctrip_driver_open']=False
    global_dict['qunar_driver_open']=False
    global_dict['consulted_flag']=False
    global_dict['searching_flag']=False
    global_dict['detailing_flag']=False
    global_dict['compare_paras']=[1,]*17
    global_dict['judger_loaded']=False
    global_dict['outporting']=False
    #当前查询状态管理
    global_dict['temp_city']=''
    global_dict['temp_check_in_date']=''
    global_dict['temp_check_out_date']=''
    global_dict['temp_destination']=''
    global_dict['temp_consult_number']=10
    global_dict['consult_city']=''
    global_dict['consult_check_in_date']=''
    global_dict['consult_check_out_date']=''
    global_dict['consult_destination']=''
    global_dict['consult_number']=10
    global_dict['comment_number']=10
    #查询结果管理
    global_dict['consulted_hotel_list']=[]
    global_dict['compare_hotel_list']=[]
    global_dict['compared_hotel_list']=[]
    #webdriver
    global_dict['ctrip_driver']=None
    global_dict['qunar_driver']=None
        #driver路径
    global_dict['driver_path']=r'C:\Users\SCUTEEXHJ\Desktop\应用程序\chromedriver61.exe'
    global_dict['chrome_path']=r'C:\Program Files\Google\Chrome\App\Google Chrome\chrome.exe'
    
def set_global(name,value): #改变全局变量
    global global_dict
    global_dict[name]=value
    
def get_global(name): #获得全局变量
    global global_dict
    return global_dict.get(name,None)

def del_global(name): #删除全局变量
    global global_dict
    try:
        del global_dict[name]
    except:
        pass