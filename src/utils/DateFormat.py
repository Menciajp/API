import datetime

class DateFormat():

    def convert_date_to_string(date):
        return datetime.datetime.strptime("%d/%m/%Y")
    
    def convert_date_to_string(date):
        return date.strftime("%Y/%m/%d")