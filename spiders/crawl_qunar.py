#导入包
    #系统包
import time #用于休息，防止访问过快被反爬
from tkinter import messagebox #用于异常梯形
import sys
sys.path.append('..')
import global_manager as gm #全局变量管理器
import exception_classes as excp_cls #自定义异常
    #自定义包
import spiders.simulation_explorer_driver as sim
import spiders.hotel_classes as hotel_cls

class consult_qunar():
    def __init__(self,load_image=False,headless=True): #初始化，打开浏览器
        if gm.get_global('qunar_driver_open'):
            temp_driver=gm.get_global('qunar_driver')
            try:
                temp_driver.quit()
            except:
                pass
        try:
            self.driver_cls=sim.consult_webdriver(load_image,headless)
        except:
            messagebox.showerror('内部错误','去哪儿网查询器未能成功打开！')
            raise excp_cls.webdriver_error
            return
        else:
            self.driver=self.driver_cls.visit_driver()
            gm.set_global('qunar_driver',self.driver)
            gm.set_global('qunar_driver_open',True)
        self.consulted_hotel_list=[]
        self.this_hotel_detail=('',)*17
        self.consulted_number=0
    
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
        #访问目标地址
        self.consulted_number=0
        city=consult_information['City']
        location=consult_information['Destination']
        check_in_date=consult_information['Check-in Date']
        check_out_date=consult_information['Check-out Date']
        dest_url='https://hotel.qunar.com/city/%s/q-%s#fromDate=%s&cityurl=%s&toDate=%s&from=qunarHotel'%(
        city,location,check_in_date,city,check_out_date)
        self.driver.get(dest_url)
        #获取总页面数量
        try:
            next_page_element=self.driver.find_element_by_css_selector('li.item.next')
        except:
            total_page_number=1
        else:
            next_page_element=self.driver.find_elements_by_css_selector('li.item')
            try:
                total_page_number=int(next_page_element[-2].text)
            except:
                total_page_number=1
        #获取各页面酒店信息
        self.consulted_hotel_list=[]
        hotel_now_index=0
        hotel_stop_flag=False
        for page_index in range(total_page_number): #对每一页
            #拉到最底部，加载全部信息
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") #滑动到页面底部，加载全部酒店
            time.sleep(1.5)
            #获取当前页面酒店信息
            hotel_list=self.driver.find_elements_by_css_selector('div.item_hotel_info')
            for each_hotel in hotel_list: #对每一个酒店对象
                hotel_now_index+=1
                hotel_detail=each_hotel.find_element_by_css_selector('div.hotel_baseinfo')
                hotel_name_callback=hotel_detail.find_element_by_xpath(".//span[@class='hotel_item']//a")
                hotel_name=hotel_name_callback.get_attribute('title') #获取酒店名称
                hotel_page_link=hotel_name_callback.get_attribute('href') #获取酒店详情页面链接
                hotel_address_description_callback=hotel_detail.find_element_by_xpath(".//span[@class='area_contair']")
                hotel_address_description=hotel_address_description_callback.text #获取酒店位置描述
                hotel_price_callback=each_hotel.find_element_by_css_selector('div.hotel_price') #获取页面显示的酒店价格
                hotel_price=hotel_price_callback.text.replace('起','').replace('元','').replace('参考价：','').replace('¥','')
                if len(hotel_price)==0:
                    hotel_price='该酒店暂无网站参考报价！'
                try:
                    hotel_no_comment_callback=hotel_detail.find_element_by_css_selector('span.no_comment')
                except:
                    hotel_score_callback=each_hotel.find_element_by_xpath(".//p[@class='score']//a//b")
                    hotel_score=hotel_score_callback.text
                    hotel_first_comment_callback=hotel_detail.find_element_by_xpath(".//p[@class='review first_review']//a")
                    hotel_first_comment=hotel_first_comment_callback.get_attribute('title')
                    hotel_comment=hotel_first_comment
                    if not len(hotel_comment):
                        hotel_comment='该酒店暂无评价！'
                    if not len(hotel_score):
                        hotel_score='0'
                else: #该酒店没有评价
                    hotel_score='0'
                    hotel_comment='该酒店暂无评价！'
                #保存信息
                this_hotel=hotel_cls.basic_hotel_info(hotel_name,hotel_address_description,hotel_price,hotel_score,hotel_comment,hotel_page_link,'','去哪儿网')
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
                next_page_button=self.driver.find_element_by_css_selector('li.item.next')
                next_page_button.click()
                time.sleep(1)
        if len(self.consulted_hotel_list)==0:
            messagebox.showinfo('温馨提示','当前搜索条件下去哪儿网没有查到酒店！')

    def get_consult_qunar_list(self): #返回查询清单
        return self.consulted_hotel_list
    
    def consult_single_hotel_qunar_core(self,single_hotel_base_obj,consult_information,consult_comment_number=10): #查询单个酒店的详细信息
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
        #反爬措施：先访问酒店查询页
        consult_city=consult_information['City']
        consult_location=consult_information['Destination']
        consult_check_in_date=consult_information['Check-in Date']
        consult_check_out_date=consult_information['Check-out Date']
        dest_url='https://hotel.qunar.com/city/%s/q-%s#fromDate=%s&cityurl=%s&toDate=%s&from=qunarHotel'%(
        consult_city,consult_location,consult_check_in_date,consult_city,consult_check_out_date)
        self.driver.get(dest_url)
        #访问目标地址
        hotel_URL=single_hotel_base_obj.return_info()[5]
        self.driver.get(hotel_URL)
        #获取详细信息
        hotel_detail=dict()
        hotel_name=single_hotel_base_obj.return_info()[0]
            #获取评分
        total_score_callback=self.driver.find_element_by_css_selector('p.score')
        try:
            no_score_callback=total_score_callback.find_element_by_xpath(".//span[@class='no']")
        except:
            total_score_callback=total_score_callback.find_element_by_css_selector('span.num')
            score_number=float(total_score_callback.text.replace('分',''))
        else:
            score_number=0.0
            #获取好评率
        try:
            favorable_rate_callback=self.driver.find_element_by_css_selector('p.ugc-desc.ugc-bold')
        except:
            hotel_favorable_rate=0.0
        else:
            favorable_rate_text=favorable_rate_callback.text.split(' ')[0]
            if favorable_rate_text.endswith('好评'):
                hotel_favorable_rate=float(favorable_rate_text.replace('%好评',''))/100
            else:
                hotel_favorable_rate=0.0
        #获取酒店房型和价钱
            #展开全部报价
        try:
            expand_price_buttons=self.driver.find_elements_by_css_selector('div.expand-quotes-td')
        except:
            pass
        else:
            for each_button in expand_price_buttons:
                each_button.click()
            #获取全部报价
        try:
            hotel_room_table_callback=self.driver.find_element_by_css_selector('div.js-room-table')
        except:
            hotel_room_price_list=dict()
        else:
            hotel_rooms_callback=hotel_room_table_callback.find_elements_by_css_selector('div.room-quote-item.clearfix')
            hotel_room_price_list=dict()
            for each_hotel_room_type in hotel_rooms_callback:
                hotel_room_type_name=each_hotel_room_type.find_element_by_css_selector('h5.room-name').text
                hotel_room_type_moneys=each_hotel_room_type.find_elements_by_css_selector('span.lowprice-money')
                hotel_room_price=[]
                for each_hotel_price_callback in hotel_room_type_moneys:
                    hotel_room_price.append(float(each_hotel_price_callback.text))
                hotel_room_price_list[hotel_room_type_name]=hotel_room_price
        #获取酒店详情
        hotel_detail_information_callback=self.driver.find_elements_by_css_selector('div.dt-module')
            #获取联系方式和简介
        hotel_first_dt_info_block=hotel_detail_information_callback[0]
        hotel_dt_info_callback=hotel_first_dt_info_block.find_elements_by_xpath(".//dl")
                #获取联系方式
        try:
            hotel_contact_callback=hotel_dt_info_callback[0].find_element_by_xpath('.//dd//span')
        except:
            hotel_contact_number=''
        else:
            hotel_contact_text=hotel_contact_callback.text
            hotel_contact_number=hotel_contact_text.split(' ')[-1]
                #获取简介
        try:
            hotel_brief_introduction_callback=hotel_dt_info_callback[-1].find_element_by_xpath('.//dd')
        except:
            hotel_brief_introduction=''
        else:
            hotel_brief_introduction=hotel_brief_introduction_callback.text
            #获取入离时间至预定须知
        hotel_second_dt_info_block=hotel_detail_information_callback[1]
        hotel_dt_info_callback=hotel_second_dt_info_block.find_elements_by_xpath('.//dl')
        second_dt_info_index=0
        total_second_dt_information_sections_num=len(hotel_dt_info_callback)
                #获取入住时间和离店时间
        if second_dt_info_index<total_second_dt_information_sections_num:
            try:
                ensure_check_inout_time_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dt')
            except:
                check_in_time='未提供'
                check_out_time='未提供'
            else:
                ensure_check_inout_time=ensure_check_inout_time_callback.text
                if ensure_check_inout_time=='入离时间':
                    hotel_check_inout_time_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dd')
                    hotel_check_inout_time_text=hotel_check_inout_time_callback.text.split(' ')
                    check_in_time=hotel_check_inout_time_text[1].replace('以后','')
                    check_out_time=hotel_check_inout_time_text[-1].replace('以前','')
                    second_dt_info_index+=1
                else:
                    check_in_time='未提供'
                    check_out_time='未提供'
        else:
            check_in_time='未提供'
            check_out_time='未提供'
            hotel_child_policy='未提供'
            hotel_extra_fee_text='未提供'
            hotel_notation='未提供'
                #获取儿童政策
        if second_dt_info_index<total_second_dt_information_sections_num:
            ensure_child_policy_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dt')
            ensure_child_policy=ensure_child_policy_callback.text
            if ensure_child_policy=='儿童政策':
                try:
                    hotel_child_policy_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dd')
                except:
                    hotel_child_policy=''
                else:
                    hotel_child_policy=hotel_child_policy_callback.text
                second_dt_info_index+=1
            else:
                hotel_child_policy='未提供'
        else:
            hotel_child_policy='未提供'
            hotel_extra_fee_text='未提供'
            hotel_notation='未提供'
                #获取附加费用
        if second_dt_info_index<total_second_dt_information_sections_num:
            ensure_extra_fee_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dt')
            ensure_extra_fee=ensure_extra_fee_callback.text
            if ensure_extra_fee=='附加费用':
                try:
                    hotel_extra_fee_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dd')
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
            ensure_notation_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dt')
            ensure_notation=ensure_notation_callback.text
            if ensure_notation=='预订须知':
                try:
                    hotel_notation_callback=hotel_dt_info_callback[second_dt_info_index].find_element_by_xpath('.//dd')
                except:
                    hotel_notation=''
                else:
                    hotel_notation=hotel_notation_callback.text
            else:
                hotel_notation='未提供'
        else:
            hotel_notation='未提供'
            #获取各类酒店设施
        hotel_third_dt_info_block=hotel_detail_information_callback[-1]
        hotel_dt_info_callback=hotel_third_dt_info_block.find_elements_by_xpath('.//dl')
        third_dt_info_index=0
        total_third_dt_information_sections_num=len(hotel_dt_info_callback)
                #获取酒店网络设施
        if third_dt_info_index<total_third_dt_information_sections_num:
            ensure_network_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dt')
            ensure_network_facility=ensure_network_facility_callback.text
            if ensure_network_facility=='网络设施':
                try:
                    hotel_network_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dd')
                except:
                    hotel_network_facility=[]
                else:
                    hotel_network_facility_text=hotel_network_facility_callback.text.replace('"','')
                    hotel_network_facility=hotel_network_facility_text
                third_dt_info_index+=1
            else:
                hotel_network_facility_text='未提供'
                hotel_network_facility=[]
        else:
            hotel_network_facility_text='未提供'
            hotel_network_facility=[]
            hotel_parking_text='未提供'
            hotel_room_facility=[]
            hotel_other_facility=[]
            hotel_service=[]
                #获取酒店停车场
        if third_dt_info_index<total_third_dt_information_sections_num:
            ensure_parking_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dt')
            ensure_parking=ensure_parking_callback.text
            if ensure_parking=='停车场':
                try:
                    hotel_parking_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dd')
                except:
                    hotel_parking_text='未提供'
                else:
                    hotel_parking_text=hotel_parking_callback.text.replace('"','')
                third_dt_info_index+=1
            else:
                hotel_parking_text='未提供'
        else:
            hotel_parking_text='未提供'
            hotel_room_facility=[]
            hotel_other_facility=[]
            hotel_service=[]
                #获取酒店房间设施
        if third_dt_info_index<total_third_dt_information_sections_num:
            ensure_room_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dt')
            ensure_room_facility=ensure_room_facility_callback.text
            if ensure_room_facility=='房间设施':
                try:
                    hotel_room_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dd')
                except:
                    hotel_room_facility=[]
                else:
                    hotel_room_facility_service_list=hotel_room_facility_callback.find_elements_by_css_selector('span.item')
                    hotel_room_facility=[]
                    for each_room_facility in hotel_room_facility_service_list:
                        hotel_room_facility.append(each_room_facility.text.replace('"',''))
                third_dt_info_index+=1
            else:
                hotel_room_facility=[]
        else:
            hotel_room_facility=[]
            hotel_other_facility=[]
            hotel_service=[]
                #获取酒店其他设施
        if third_dt_info_index<total_third_dt_information_sections_num:
            ensure_other_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dt')
            ensure_other_facility=ensure_other_facility_callback.text
            if ensure_other_facility=='酒店设施':
                try:
                    hotel_other_facility_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dd')
                except:
                    hotel_other_facility=[]
                else:
                    hotel_other_facility_service_list=hotel_other_facility_callback.find_elements_by_css_selector('span.item')
                    hotel_other_facility=[]
                    for each_other_facility in hotel_other_facility_service_list:
                        hotel_other_facility.append(each_other_facility.text.replace('"',''))
                third_dt_info_index+=1
            else:
                hotel_other_facility=[]
        else:
            hotel_other_facility=[]
            hotel_service=[]
                #获取酒店服务
        if third_dt_info_index<total_third_dt_information_sections_num:
            try:
                ensure_service_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dt')
            except:
                hotel_service=[]
            else:
                ensure_service=ensure_service_callback.text
                if ensure_service=='酒店服务':
                    try:
                        hotel_service_callback=hotel_dt_info_callback[third_dt_info_index].find_element_by_xpath('.//dd')
                    except:
                        hotel_service=[]
                    else:
                        hotel_service_list=hotel_service_callback.find_elements_by_css_selector('span.item')
                        hotel_service=[]
                        for each_service in hotel_service_list:
                            hotel_service.append(each_service.text.replace('"',''))
                else:
                    hotel_service=[]
        else:
            hotel_service=[]
        #获取酒店评价
            #总页数
        try:
            comment_page_total_number_callback=self.driver.find_element_by_css_selector('div.pager')
        except:
            total_page_number=0
        else:
            try:
                last_page_button_callback=comment_page_total_number_callback.find_element_by_css_selector('div.item.first-item.last-item')
            except:
                total_page_number=1
            else:
                try:
                    total_page_number=int(last_page_button_callback.text)
                except:
                    total_page_number=0
            #开始获取酒店评价
        hotel_comment_list=[]
        comment_now_index=0
        comment_stop_flag=False
        for comment_page in range(total_page_number):
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") #滑动到页面底部，加载全部评论
            comment_content_block_callback_list=self.driver.find_elements_by_css_selector('div.cmt-content') #一条评价的模块
            for each_comment_block_callback in comment_content_block_callback_list: #每一个评价
                comment_now_index+=1
                comment_content_callback=each_comment_block_callback.find_element_by_css_selector('p.js_contentAll')
                comment_content=comment_content_callback.text
                comment_date_callback=each_comment_block_callback.find_element_by_xpath(".//p[@class='ct-extra']//span")
                comment_date_text=comment_date_callback.text
                comment_date=comment_date_text.replace(' ','').split('|')[1]
                comment_date=comment_date.replace('发表于','')
                comment_date=comment_date.replace('年','-').replace('月','-').replace('日','')
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
                next_page_button_element=self.driver.find_element_by_css_selector('div.item.next.js_next.abled')
                next_page_button_element.click()
                time.sleep(1)
        #保存查询结果
        self.this_hotel_detail=hotel_cls.detail_hotel_info(hotel_name,score_number,hotel_favorable_rate,hotel_room_price_list,
                               check_in_time,check_out_time,hotel_contact_number,hotel_brief_introduction,
                               hotel_child_policy,hotel_extra_fee_text,hotel_notation,hotel_network_facility_text,
                               hotel_parking_text,hotel_room_facility,hotel_other_facility,hotel_service,hotel_comment_list)

    def get_consult_qunar_single_hotel(self): #返回查到的具体内容
        info=self.this_hotel_detail.return_info()
        return info