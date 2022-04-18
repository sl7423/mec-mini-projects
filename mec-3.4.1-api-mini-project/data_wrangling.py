import json
import urllib.request

class Authentication:
    ...

class NasdaqRequest:
    def __init__(self, website, exchange, ticker):
        self.website = website
        self.exchange = exchange
        self.ticker = ticker

    def load_json(self, style):
        url_page = self.website + self.exchange + "/" + self.ticker + ".json"
        data = json.loads(urllib.request.urlopen(url_page).read().decode(style))
        return data

class NasdaqFilter:
    def __init__(self, data:dict):
        self.data = data['dataset']
        self.combined = {}
        self.headers = data['dataset']['column_names']

    def return_columns(self):
        return self.data.keys()
    
    def date_filter(self, range_1=None, range_2=None):
        date_index = self.headers.index('Date')
        for number in range(len(self.headers)):
            self.combined[self.headers[number]] = []
    
        for lst in self.data['data']:
            if lst[date_index] > range_1 and lst[date_index] <= range_2:
                for number in range(len(self.headers)):
                    self.combined[self.headers[number]].append(lst[number])

        return self.combined

class Math:
    @staticmethod
    def average(dic, title):
        lst = dic[title]
        total = sum(value for value in lst if isinstance(value, float))
        return round(total/len(lst), 2)

    @staticmethod
    def max(dic, title):
        lst = dic[title]
        return round(max(value for value in lst if isinstance(value, float)),2)

    @staticmethod
    def min(dic, title):
        lst = dic[title]
        return round(min(value for value in lst if isinstance(value, float)),2)

    @staticmethod
    def find_diff_values(dic, title):
        lst = dic[title]
        diff_value = 0
        for value in range(len(lst)):
            if lst[value] is None:
                lst[value] = 0
            if value > 0 and (lst[value] - lst[value-1]) > diff_value:
                diff_value = lst[value] - lst[value-1]
        return diff_value
        

    @staticmethod
    def find_diff_list(dic1, title1, dic2, title2):
        combined_1 = dic1[title1]
        combined_2 = dic2[title2]
        if len(combined_1) != len(combined_2):
            raise ValueError("Length of the Two List is NOT the same!")
        max_value = 0
        for value in range(len(combined_1)):
            if combined_1[value] is None:
                combined_1[value] = 0
            if combined_2[value] is None:
                combined_2[value] = 0
            new_value = combined_1[value] - combined_2[value]
            if new_value > max_value:
                max_value = new_value
        return max_value
        

if __name__ == '__main__':

    URL = 'https://data.nasdaq.com/api/v3/datasets/'
    EXCHANGE = 'FSE'
    TICKER = 'AFX_X'
    
    AFX = NasdaqRequest(URL, EXCHANGE, TICKER)
    data = NasdaqFilter(AFX.load_json('utf8')).date_filter('2017-01-01','2017-12-31')
    print(Math.average(data,"Traded Volume"))
    print(Math.max(data, "Open"))
    print(Math.min(data,'Open'))
    print(Math.find_diff_list(data, "Open", data, "Close"))
    print(Math.find_diff_values(data,"Traded Volume"))