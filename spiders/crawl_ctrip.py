#导入包
    #系统包
from selenium.webdriver.common.keys import Keys #支持键盘输入
import time #用于休息，防止访问过快被反爬
from tkinter import messagebox #用于异常提示
import sys
sys.path.append('..')
import global_manager as gm #全局变量管理器
import exception_classes as excp_cls #自定义异常
    #自定义包
import spiders.simulation_explorer_driver as sim
import spiders.hotel_classes as hotel_cls

class consult_ctrip():
    def __init__(self,load_images=False,headless=True): #初始化，打开浏览器
        if gm.get_global('ctrip_driver_open'):
            temp_driver=gm.get_global('ctrip_driver')
            try:
                temp_driver.quit()
            except:
                pass
        try:
            self.driver_cls=sim.consult_webdriver(load_images,headless)
        except:
            messagebox.showerror('内部错误','携程网查询器未能成功打开！')
            raise excp_cls.webdriver_error
            return
        else:
            self.driver=self.driver_cls.visit_driver()
            gm.set_global('ctrip_driver',self.driver)
            gm.set_global('ctrip_driver_open',True)
        self.consulted_hotel_list=[]
        self.consulted_number=0
        self.this_hotel_detail=('',)*17
            
    def consult_hotels_core(self,consult_information,consult_hotel_number=10): #爬取总概要
        #检查查询数量
        if isinstance(consult_hotel_number,str) and consult_hotel_number.lower()=='all':
            consult_forever_flag=True
        else:
            consult_forever_flag=False
            if isinstance(consult_hotel_number,str):
                try:
                    consult_hotel_number=int(eval(consult_hotel_number))
                except:
                    messagebox.showinfo('温馨提示','查询酒店数目输入错误,已内部修正为10！')
                    consult_hotel_number=10
            else:
                consult_hotel_number=int(consult_hotel_number)
                if consult_hotel_number<=0:
                    messagebox.showinfo('温馨提示','查询酒店数目输入错误,已内部修正为10！')
                    consult_hotel_number=10
        #获取查询信息
        self.consulted_number=0
        city=consult_information['City']
        location=consult_information['Destination']
        check_in_date=consult_information['Check-in Date']
        check_out_date=consult_information['Check-out Date']
        #获取酒店列表页
            #因为携程查询网址没有规律，因此要从酒店首页开始查
        self.driver.get('https://hotels.ctrip.com/')
            #把信息送入携程查询栏并查询
        city_input_box=self.driver.find_element_by_id('txtCity')
        city_input_box.clear()
        city_input_box.send_keys(city)
        check_in_date_input_box=self.driver.find_element_by_id('txtCheckIn')
        check_in_date_input_box.clear()
        check_in_date_input_box.send_keys(check_in_date)
        check_out_date_input_box=self.driver.find_element_by_id('txtCheckOut')
        check_out_date_input_box.clear()
        check_out_date_input_box.send_keys(check_out_date)
        location_input_box=self.driver.find_element_by_id('txtKeyword')
        location_input_box.clear()
        location_input_box.send_keys(location)
        location_input_box.send_keys(Keys.ENTER)
            #获取总页数
        try:
            page_bar_callback=self.driver.find_element_by_css_selector('div.c_page_list.layoutfix')
        except:
            total_page_number=1
        else:
            page_buttons=page_bar_callback.find_elements_by_xpath('.//a')
            total_page_number=int(page_buttons[-1].text)
        #获取各页酒店信息
        self.consulted_hotel_list=[]
        hotel_now_index=0
        hotel_stop_flag=False
        for page_index in range(total_page_number): #对每一页
            #拉到最底部，加载全部信息
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") #滑动到页面底部，加载全部酒店
            time.sleep(1.5)
            #获取当前页面酒店信息
            hotel_list=self.driver.find_elements_by_css_selector('div.hotel_new_list.J_HotelListBaseCell')
            for each_hotel in hotel_list: #对每一个酒店对象
                hotel_now_index+=1
                hotel_name_callback=each_hotel.find_element_by_xpath(".//ul//li[@class='hotel_item_name']//h2[@class='hotel_name']//a")
                hotel_name=hotel_name_callback.get_attribute('title') #获取酒店名称
                hotel_page_link=hotel_name_callback.get_attribute('href') #获取酒店链接
                hotel_address_description_callback=each_hotel.find_element_by_xpath(".//ul//li[@class='hotel_item_name']//p[@class='hotel_item_htladdress']")
                hotel_address_description=hotel_address_description_callback.text.replace(' 地图','').replace('街景','').replace('】',' ').replace('【',' ').replace('\n','').replace(' ','').replace('\t','') #获取酒店位置描述
                hotel_price_callback=each_hotel.find_element_by_css_selector('span.J_price_lowList')
                hotel_price=hotel_price_callback.text #获取酒店最低价格
                try:
                    hotel_score_callback=each_hotel.find_element_by_css_selector('span.hotel_value')
                except:
                    hotel_score='0'
                else:
                    hotel_score=hotel_score_callback.text #获取酒店评分
                if len(hotel_score)==0:
                    hotel_score='0'
                try:
                    hotel_favorable_rate_callback=each_hotel.find_element_by_css_selector('span.total_judgement_score')
                except:
                    hotel_favorable_rate='0.0'
                else:
                    hotel_favorable_rate_callback=hotel_favorable_rate_callback.find_element_by_xpath('.//span')
                    hotel_favorable_rate=hotel_favorable_rate_callback.text.replace('%','')
                if len(hotel_favorable_rate)==0:
                    hotel_favorable_rate='0.0'
                try:
                    hotel_comment_callback=each_hotel.find_element_by_css_selector('span.recommend')
                except:
                    hotel_comment='该酒店暂无评价！'
                    hotel_score='0'
                else:
                    hotel_comment=hotel_comment_callback.text.replace('\n','') #获取酒店评价
                #保存信息
                this_hotel=hotel_cls.basic_hotel_info(hotel_name,hotel_address_description,hotel_price,hotel_score,hotel_comment,hotel_page_link,hotel_favorable_rate,'携程网')
                self.consulted_hotel_list.append(this_hotel)
                self.consulted_number+=1
                #增加索引值，判断是否达到需要查询的酒店总数量
                if not consult_forever_flag:
                    if hotel_now_index==consult_hotel_number:
                        hotel_stop_flag=True
                        break
            #已经查询到了需要数目的酒店，停止查询
            if not consult_forever_flag and hotel_stop_flag:
                break
            #翻下一页
            if page_index!=total_page_number-1:
                try:
                    last_price_callback=self.driver.find_element_by_xpath("//div[@class='searchresult_list tuan_recommend']//ul//li//div//span")
                except:
                    last_price_callback=hotel_list[-1]
                js="arguments[0].scrollIntoView();"
                self.driver.execute_script(js,last_price_callback)
                next_page_button=self.driver.find_element_by_id('downHerf')
                next_page_button.click()
                time.sleep(1)
        if len(self.consulted_hotel_list)==0:
            messagebox.showinfo('温馨提示','当前搜索条件下携程网没有查到酒店！')
    
    def get_consult_ctrip_list(self): #返回查询清单
        return self.consulted_hotel_list
    
    def consult_single_hotel_ctrip_core(self,single_hotel_base_obj,consult_information,consult_comment_number=10): #查询单个酒店的详细信息
        #检查查询数量
        if isinstance(consult_comment_number,str) and consult_comment_number.lower()=='all':
            consult_forever_flag=True
        else:
            consult_forever_flag=False
            if isinstance(consult_forever_flag,str):
                try:
                    consult_comment_number=int(eval(consult_comment_number))
                except:
                    messagebox.showinfo('温馨提示','查询评价数目输入错误,已内部修正为10！')
                    consult_comment_number=10
            else:
                consult_comment_number=int(consult_comment_number)
                if consult_comment_number<=0:
                    messagebox.showinfo('温馨提示','查询评价数目输入错误,已内部修正为10！')
                    consult_comment_number=10
        #反爬措施：先查询酒店列表
            #获取查询信息
        city=consult_information['City']
        location=consult_information['Destination']
        check_in_date=consult_information['Check-in Date']
        check_out_date=consult_information['Check-out Date']
            #获取酒店列表页
                #因为携程查询网址没有规律，因此要从酒店首页开始查
        self.driver.get('https://hotels.ctrip.com/')
                #把信息送入携程查询栏并查询
        city_input_box=self.driver.find_element_by_id('txtCity')
        city_input_box.clear()
        city_input_box.send_keys(city)
        check_in_date_input_box=self.driver.find_element_by_id('txtCheckIn')
        check_in_date_input_box.clear()
        check_in_date_input_box.send_keys(check_in_date)
        check_out_date_input_box=self.driver.find_element_by_id('txtCheckOut')
        check_out_date_input_box.clear()
        check_out_date_input_box.send_keys(check_out_date)
        location_input_box=self.driver.find_element_by_id('txtKeyword')
        location_input_box.clear()
        location_input_box.send_keys(location)
        location_input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        #访问目标地址
        hotel_URL=single_hotel_base_obj.return_info()[5]
        self.driver.get(hotel_URL)
        #滑到页面底部
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") #滑动到页面底部，加载全部评论
        time.sleep(1)
        #获取详细信息
        hotel_name=single_hotel_base_obj.return_info()[0]
            #获取评分
        try:
            total_score_callback=self.driver.find_element_by_css_selector('div.htl_com_box.basefix')
            total_score_callback=total_score_callback.find_element_by_xpath(".//a//p//span")
        except:
            score_number=0.0
        try:
            score_number=float(total_score_callback.text)
        except:
            score_number=0.0
            #获取好评率
        hotel_favorable_rate_text=single_hotel_base_obj.return_info()[6]
        try:
            hotel_favorable_rate=float(hotel_favorable_rate_text)/100
        except:
            hotel_favorable_rate=0.0
        #获取酒店房型和价钱
        try:
            hotel_room_table_callback=self.driver.find_element_by_id('J_RoomListTbl')
            hotel_rooms_callback=hotel_room_table_callback.find_elements_by_xpath('.//tbody//tr')
        except:
            hotel_room_price_list=dict()
        else:
            hotel_price_start_record_flag=False
            next_room_is_new_type=True
            hotel_room_price_list=dict()
            for each_hotel_room_type in hotel_rooms_callback:
                this_type_text=each_hotel_room_type.text
                if this_type_text=='符合条件的房型' and (not hotel_price_start_record_flag):
                    hotel_price_start_record_flag=True
                    continue
                if hotel_price_start_record_flag:
                    this_item_class_name=each_hotel_room_type.get_attribute('class')
                    if this_item_class_name=='clicked hidden': #反爬对抗
                        continue
                    if next_room_is_new_type:
                        hotel_room_type_name_callback=each_hotel_room_type.find_element_by_css_selector('a.room_unfold.J_show_room_detail')
                        hotel_room_type_name=hotel_room_type_name_callback.text.replace('查看详情','').replace('\n','')
                        hotel_room_price=[]
                        hotel_room_price_callback=each_hotel_room_type.find_element_by_css_selector('span.base_txtdiv')
                        hotel_room_price_text=hotel_room_price_callback.text.replace('¥','')
                        hotel_room_price.append(float(hotel_room_price_text))
                    else:
                        hotel_room_price_callback=each_hotel_room_type.find_element_by_css_selector('span.base_txtdiv')
                        hotel_room_price_text=hotel_room_price_callback.text.replace('¥','')
                        hotel_room_price.append(float(hotel_room_price_text))
                    if 'last_room' in this_item_class_name: #判断是否为该房型的最后一个价格
                        next_room_is_new_type=True
                        hotel_room_price_list[hotel_room_type_name]=hotel_room_price
                    else:
                        next_room_is_new_type=False
        #获取酒店详情
            #获取联系方式和简介
                #获取联系方式
        try:
            hotel_contact_callback=self.driver.find_element_by_id('J_realContact')
        except:
            hotel_contact_number='未提供'
        else:
            hotel_contact_text=hotel_contact_callback.get_attribute('data-real')
            hotel_contact_number=hotel_contact_text.split(' ')[0].replace('电话','')
                #获取简介
        try:
            hotel_brief_introduction_callback=self.driver.find_element_by_id('htlDes')
        except:
            hotel_brief_introduction='未提供'
        else:
            hotel_brief_introduction_callback=hotel_brief_introduction_callback.find_element_by_xpath(".//span[@itemprop='description']")
            hotel_brief_introduction=hotel_brief_introduction_callback.text.replace(' ','').replace('\n','')
            #获取入离时间至预定须知
        hotel_detail_information_callback=self.driver.find_elements_by_css_selector('div.htl_info_table')
        hotel_second_dt_info_block=hotel_detail_information_callback[1]
        hotel_dt_info_callback=hotel_second_dt_info_block.find_elements_by_xpath('.//table//tbody//tr')
        second_dt_info_index=0
        total_second_dt_information_sections_num=len(hotel_dt_info_callback)
                #获取入离时间
        if second_dt_info_index<total_second_dt_information_sections_num:
            try:
                ensure_check_inout_time_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//th')
            except:
                check_in_time='未提供'
                check_out_time='未提供'
            else:
                ensure_check_inout_time=ensure_check_inout_time_callback.text
                if ensure_check_inout_time=='入住和离店':
                    try:
                        hotel_check_inout_time_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//td')
                    except:
                        check_in_time='未提供'
                        check_out_time='未提供'
                    else:
                        hotel_check_inout_time_text=hotel_check_inout_time_callback.text.split(' ')
                        check_in_time=hotel_check_inout_time_text[0].replace('以后','').replace('入住时间：','')
                        check_out_time=hotel_check_inout_time_text[-1].replace('以前','').replace('离店时间：','')
                    second_dt_info_index+=1
                else:
                    check_in_time='未提供'
                    check_out_time='未提供'
        else:
            check_in_time='未提供'
            check_out_time='未提供'
            hotel_child_policy=[]
            hotel_extra_fee_text='未提供'
            hotel_notation='未提供'
                #获取儿童政策
        if second_dt_info_index<total_second_dt_information_sections_num:
            try:
                ensure_child_policy_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//th')
            except:
                hotel_child_policy=[]
            else:
                ensure_child_policy=ensure_child_policy_callback.text
                if ensure_child_policy=='儿童政策':
                    try:
                        hotel_child_policy_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//td')
                    except:
                        hotel_child_policy=[]
                    else:
                        hotel_child_policy=hotel_child_policy_callback.text.replace('\n','').split('•')
                    second_dt_info_index+=1
                else:
                    hotel_child_policy=[]
                while '' in hotel_child_policy:
                    hotel_child_policy.remove('')
        else:
            hotel_child_policy=[]
            hotel_extra_fee_text='未提供'
            hotel_notation='未提供'
                #获取附加费用
        if second_dt_info_index<total_second_dt_information_sections_num:
            ensure_extra_fee_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//th')
            ensure_extra_fee=ensure_extra_fee_callback.text
            if ensure_extra_fee=='早餐信息':
                try:
                    hotel_extra_fee_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//td')
                except:
                    hotel_extra_fee_text='未提供'
                else:
                    hotel_extra_fee_text=hotel_extra_fee_callback.text
                second_dt_info_index+=1
            else:
                hotel_extra_fee_text='未提供'
        else:
            hotel_extra_fee_text='未提供'
            hotel_notation='未提供'
                #获取其它预定须知
        if second_dt_info_index<total_second_dt_information_sections_num:
            ensure_notation_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//th')
            ensure_notation=ensure_notation_callback.text
            if ensure_notation=='宠物':
                try:
                    hotel_notation_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//td')
                except:
                    hotel_notation='未提供'
                else:
                    hotel_notation=hotel_notation_callback.text
            else:
                hotel_notation='未提供'
        else:
            hotel_notation='未提供'
            #获取各类酒店设施
        hotel_third_dt_info_block=hotel_detail_information_callback[0]
        hotel_dt_info_callback=hotel_third_dt_info_block.find_elements_by_xpath('.//table//tbody//tr')
        third_dt_info_index=0
        total_third_dt_information_sections_num=len(hotel_dt_info_callback)
                #获取酒店网络设施
        if third_dt_info_index<total_third_dt_information_sections_num:
            ensure_network_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//th')
            ensure_network_facility=ensure_network_facility_callback.text
            if ensure_network_facility=='网络':
                hotel_network_facility_text=[]
                try:
                    hotel_network_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_elements_by_xpath('.//td//ul//li')
                except:
                    pass
                else:
                    for each_network_facility in hotel_network_facility_callback:
                        hotel_network_facility_text.append(each_network_facility.text.replace('\n','').replace(' ',''))
                third_dt_info_index+=1
            else:
                hotel_network_facility_text=[]
        else:
            hotel_network_facility_text=[]
            hotel_parking_text='未提供'
            hotel_room_facility=[]
            hotel_other_facility=[]
            hotel_service=[]
        #获取酒店停车场
        if third_dt_info_index<total_third_dt_information_sections_num:
            ensure_parking_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//th')
            ensure_parking=ensure_parking_callback.text
            if ensure_parking=='交通设施':
                try:
                    hotel_parking_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath(".//td//ul//li[@class='fac-long']")
                    hotel_parking_span_text_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath(".//td//ul//li[@class='fac-long']//span")
                except:
                    hotel_parking_text='未提供'
                else:
                    hotel_parking_text=hotel_parking_callback.text.replace(hotel_parking_span_text_callback.text,'')
                third_dt_info_index+=1
            else:
                hotel_parking_text='未提供'
        else:
            hotel_parking_text='未提供'
            hotel_room_facility=[]
            hotel_other_facility=[]
            hotel_service=[]
                #获取酒店房间设施--携程不提供
        hotel_room_facility=[]
                #获取酒店其他设施以及酒店服务
        hotel_other_facility=[]
        hotel_service=[]
                    #先展开全部内容
        try:
            expand_button_callback=self.driver.find_element_by_id('J_show_unfold')
        except:
            pass
        else:
            detail_title_callback=self.driver.find_elements_by_css_selector('h2.detail_title')
            detail_title_callback=detail_title_callback[1]
            js="arguments[0].scrollIntoView();"
            self.driver.execute_script(js,detail_title_callback)
            expand_button_callback.click()
                    #获取全部内容
        for each_hotel_info_element in hotel_dt_info_callback:
            try:
                title_text=each_hotel_info_element.find_element_by_xpath(".//th").text
            except:
                continue
            if "通用设施" in title_text:
                hotel_other_facilities_callback=each_hotel_info_element.find_elements_by_xpath(".//td//ul//li")
                for each_facility in hotel_other_facilities_callback:
                    hotel_other_facility.append(each_facility.text.replace('"','').replace('\n',''))
            elif "商务服务" in title_text:
                hotel_other_facilities_callback=each_hotel_info_element.find_elements_by_xpath(".//td//ul//li")
                for each_facility in hotel_other_facilities_callback:
                    hotel_other_facility.append(each_facility.text.replace('"','').replace('\n',''))
            elif "交通服务" in title_text:
                hotel_service_callback=each_hotel_info_element.find_elements_by_xpath(".//td//ul//li")
                for each_service in hotel_service_callback:
                    hotel_service.append(each_service.text.replace('"','').replace('\n',''))
            elif "前台服务" in title_text:
                hotel_service_callback=each_hotel_info_element.find_elements_by_xpath(".//td//ul//li")
                for each_service in hotel_service_callback:
                    hotel_service.append(each_service.text.replace('"','').replace('\n',''))
            elif "餐饮服务" in title_text:
                hotel_service_callback=each_hotel_info_element.find_elements_by_xpath(".//td//ul//li")
                for each_service in hotel_service_callback:
                    hotel_service.append(each_service.text.replace('"','').replace('\n',''))
            elif "其他服务" in title_text:
                hotel_service_callback=each_hotel_info_element.find_elements_by_xpath(".//td//ul//li")
                for each_service in hotel_service_callback:
                    hotel_service.append(each_service.text.replace('"','').replace('\n',''))
        while '' in hotel_other_facility:
            hotel_other_facility.remove('')
        while '' in hotel_service:
            hotel_service.remove('')
        #获取评价
            #总页数
        try:
            comment_page_total_number_callback=self.driver.find_element_by_css_selector('div.c_page_list.layoutfix')
        except:
            total_page_number=0
        else:
            try:
                last_page_button_callback=comment_page_total_number_callback.find_elements_by_xpath(".//a")[-1]
            except:
                total_page_number=1
            else:
                total_page_number=int(last_page_button_callback.text)
            #开始获取酒店评价
        hotel_comment_list=[]
        comment_now_index=0
        comment_stop_flag=False
        for comment_page in range(total_page_number):
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") #滑动到页面底部，加载全部评论
            comment_content_block_callback_list=self.driver.find_elements_by_css_selector('div.comment_main') #一条评价的模块
            for each_comment_block_callback in comment_content_block_callback_list: #每一个评价
                comment_now_index+=1
                comment_content_callback=each_comment_block_callback.find_element_by_css_selector('div.J_commentDetail')
                comment_content=comment_content_callback.text
                comment_date_callback=each_comment_block_callback.find_element_by_css_selector('p.comment_bar_info')
                comment_date_text=comment_date_callback.text
                comment_date=comment_date_text.replace('发表于','')
                comment_date=comment_date.split('-')
                comment_year=int(comment_date[0])
                comment_month=int(comment_date[1])
                comment_day=int(comment_date[2])
                comment_date=(comment_year,comment_month,comment_day)
                this_comment=dict()
                this_comment['Content']=comment_content
                this_comment['Date']=comment_date
                hotel_comment_list.append(this_comment)
                if not consult_forever_flag:
                    if comment_now_index==consult_comment_number: #达到既定数目，不用继续爬取
                        comment_stop_flag=True
                        break
            if not consult_forever_flag and comment_stop_flag:
                break
            #翻下一页
            if comment_page!=total_page_number-1:
                #先滑到最后一个点评的位置，以免点错
                last_comment_callback=comment_content_block_callback_list[-1].find_element_by_css_selector('div.J_commentDetail')
                js="arguments[0].scrollIntoView();"
                self.driver.execute_script(js,last_comment_callback)
                #点击下一页按钮
                next_page_button_callback=self.driver.find_element_by_css_selector('a.c_down')
                next_page_button_callback.click()
        #保存查询结果
        self.this_hotel_detail=hotel_cls.detail_hotel_info(hotel_name,score_number,hotel_favorable_rate,hotel_room_price_list,
                               check_in_time,check_out_time,hotel_contact_number,hotel_brief_introduction,
                               hotel_child_policy,hotel_extra_fee_text,hotel_notation,hotel_network_facility_text,
                               hotel_parking_text,hotel_room_facility,hotel_other_facility,hotel_service,hotel_comment_list)

    def get_consult_ctrip_single_hotel(self): #返回查到的具体内容
        info=self.this_hotel_detail.return_info()
        return info