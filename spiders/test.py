import crawl_ctrip
import crawl_qunar
import sys
sys.path.append('..')
import global_manager as gm

gm.initial_global_dict()
gm.set_global('driver_path',r'C:\Users\SCUTEEXHJ\Desktop\应用程序\chromedriver61.exe')
gm.set_global('chrome_path',r'C:\Program Files\Google\Chrome\App\Google Chrome\chrome.exe')
gm.set_global('webdriver_number',0)
gm.set_global('webdriver_container',[])
gm.set_global('ctrip_consult_number',0)
consult_dict={'City':'广州','Destination':'华南理工大学','Check-in Date':'2020-01-12','Check-out Date':'2020-01-13'}
t=crawl_ctrip.consult_ctrip()
t.consult_hotels_core(consult_information=consult_dict)
hotel_list=t.get_consult_ctrip_list()
print(hotel_list[0].return_info())
consult_dict['City']='guangzhou'
p=crawl_qunar.consult_qunar()
p.consult_hotels_core(consult_information=consult_dict)
hotel_list=p.get_consult_ctrip_list()
print(hotel_list[0].return_info())
del t
del p