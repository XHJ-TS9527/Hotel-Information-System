class basic_hotel_info():
    def __init__(self,name,address,price,score,comment,url,favorable_rate,origin):
        self.__name=name
        self.__address=address
        self.__price=price
        self.__score=score
        self.__comment=comment
        self.__url=url
        self.__favorable=favorable_rate
        self.__origin=origin
        
    def return_info(self):
        return (self.__name,self.__address,self.__price,self.__score,self.__comment,self.__url,self.__favorable,self.__origin)
    
class detail_hotel_info():
    def __init__(self,name,total_score,favorable_rate,price_list,check_in_time,check_out_time,\
                 contact_number,brief_introduction,child_policy,extra_fee,notation,\
                 network_facility,parking,room_facility,other_facility,service,comment):
        self.__name=name
        self.__total_score=total_score
        self.__favorable_rate=favorable_rate
        self.__price_list=price_list
        self.__check_in_time=check_in_time
        self.__check_out_time=check_out_time
        self.__contact_number=contact_number
        self.__brief_introduction=brief_introduction
        self.__child_policy=child_policy
        self.__extra_fee=extra_fee
        self.__notation=notation
        self.__network_facility=network_facility
        self.__parking=parking
        self.__room_facility=room_facility
        self.__other_facility=other_facility
        self.__service=service
        self.__comment=comment
        
    def return_info(self):
        return (self.__name,self.__total_score,self.__favorable_rate,self.__price_list,
                self.__check_in_time,self.__check_out_time,self.__contact_number,
                self.__brief_introduction,self.__child_policy,self.__extra_fee,
                self.__notation,self.__network_facility,self.__parking,
                self.__room_facility,self.__other_facility,self.__service,self.__comment)