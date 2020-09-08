#导入包
import time #用于休息
from xpinyin import Pinyin #用于将城市转换为拼音

def consult_city_list_qunar(driver): #用于返回城市拼音映射清单，得到txt后再手动修改
    pinyin=Pinyin()
    city_pinyin_map_dict=dict()
    driver.get('https://hotel.qunar.com/')
    tocity_searchbox=driver.find_element_by_xpath("//input[@id='toCity']")
    tocity_searchbox.click()
    time.sleep(0.3) #等待城市选择框出现
    city_alphabets=driver.find_element_by_xpath("//div[@class='b_hct_nav']")
    city_alphabets=city_alphabets.find_elements_by_xpath(".//span")
    del city_alphabets[0]
    hotel_city_box=driver.find_elements_by_css_selector('div.b_hct_lst')
    del hotel_city_box[0]
    for alphabet_type_index in range(len(hotel_city_box)): #获取每个首字母分类下的城市清单
        each_alphabet_type=city_alphabets[alphabet_type_index]
        each_alphabet_type.click() #点击该字母用于使对应的城市列表处于活动状态
        city_block=driver.find_elements_by_xpath("//div[@id='TG_PANEL_%d']//dl"%(alphabet_type_index+1))
        for each_alphabet_list in city_block:
            cities=each_alphabet_list.find_elements_by_xpath(".//dd//li")
            for each_city in cities:
                city_Chinese=each_city.text
                city_Pinyin=pinyin.get_pinyin(city_Chinese.replace('市','').replace('县','').replace('旗',''),'')
                city_pinyin_map_dict[city_Chinese]=city_Pinyin
    return city_pinyin_map_dict,driver

def change_file(origin_file,target_file): #用于将得到的txt清单转化为字典，方便直接复制到python编辑器中
    file=open(origin_file,'rt')
    city_list=file.readlines()
    file.close()
    for index in range(len(city_list)):
        content=city_list[index]
        content=content.split(',')
        content[0]='"'+content[0]+'"'
        content[1]='"'+content[1].replace('\n','')+'",\n'
        content=':'.join(content)
        city_list[index]=content
    file=open(target_file,'wt')
    file.writelines(city_list)
    file.close()