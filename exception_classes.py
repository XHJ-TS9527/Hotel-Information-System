class webdriver_error(Exception): #浏览器打开错误类：版本不正确
    def __init__(self):
        super().__init__(self)
    def __str__(self):
        return ''

class consult_hotels_error(Exception): #查询错误信息
    def __init__(self):
        super().__init__(self)
    def __str__(self):
        return ''