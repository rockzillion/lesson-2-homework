import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_content(request_url):
    # 伪装身份
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

#解析投诉
def analysis(soup):
    # 创建DataFrame
    df = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
    # 找到完整的投诉信息框
    temp = soup.find('div',class_="tslb_b")
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        # 提取汽车投诉信息
        td_list = tr.find_all('td')
        #如果没有td，就是表头
        if len(td_list) > 0:
            id,brand,car_model,type,desc,problem,datetime,status = \
                td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text,\
                td_list[4].text,td_list[5].text,td_list[6].text,td_list[7].text,
            #print(id,brand,car_model,type,desc,problem,datetime,status)
            temp = {}
            temp['id']= id
            temp['brand']= brand
            temp['car_model']=car_model
            temp['type']= type
            temp['desc']=desc
            temp['problem']=problem
            temp['datetime']=datetime
            temp['status']=status
            df = df.append(temp,ignore_index=True)
    return df

result = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])             

base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
page_num = 20
for i in range(page_num):
    request_url =base_url + str(i+1) + '.shtml'
    #得到soup解析
    soup = get_page_content(request_url)
    df = analysis(soup)
    result = result.append(df)
print(result)
result.to_csv('car_complain.csv',index=False)
result.to_excel('car_complain.xlsx',index=False)