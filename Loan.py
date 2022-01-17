import itertools


class Loan:
    id_iter = itertools.count()
    def __init__(self, item_pic, item_name,start_date, end_date, customer_name):

        self.__id = next(Loan.id_iter)
        self.__item_pic = item_pic
        self.__item_name = item_name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__customer_name = customer_name

    def get_id(self):
        return self.__id

    def get_item_pic(self):
        return self.__item_pic

    def get_item_name(self):
        return self.__item_name

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_customer_name(self):
        return self.__customer_name



    def set_id(self, id):
        self.__id = id
    def set_item_pic(self, item_pic):
        self.__item_pic = item_pic

    def set_item_name(self, item_name):
        self.__item_name = item_name

    def set_start_date(self, start_date):
        self.__start_date= start_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name

