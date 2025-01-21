import datetime

class DateFormat():
    @staticmethod
    def convert_date_to_string(date):
        return date.strftime("%d/%m/%Y")
    
    # def convert_date_to_string(date):
    #     return date.strftime("%Y/%m/%d")