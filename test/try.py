import configparser
import pandas
def pands_csv():
    df = pandas.read_csv("test16.csv")
    df.replace("\r\n",'<br>', inplace=True,regex = True)
    df.replace("1(High)",'Critical', inplace=True)
    df.replace("2(Medium)",'Major', inplace=True)
    df.replace("3(Low)",'Minor', inplace=True)
    data = df.to_dict(orient = 'records')
    return data
def pands_excel():
    df = pandas.read_excel("SRTT.xls")
    df.replace("",'', inplace=True,regex = True)
    data_excel = df.to_dict(orient = 'records')
    return data_excel

data=pands_csv()
data1=pands_excel()


def get_page(offset=0, per_page=10):
    return data[offset: offset + per_page]

def get_page1(offset=0, per_page=10):
    return data1[offset: offset + per_page]