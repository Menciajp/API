

class DateFormat():
    @staticmethod
    def convert_date_to_string(date):
        return date.strftime("%d/%m/%Y")
    
    @staticmethod
    def convert_date_for_database(date):
        return date.strftime("%Y/%m/%d")