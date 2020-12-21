from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
import datetime
import urllib.request
import urllib.parse
# Create your views here.

from django.conf import settings
import os
import pandas as pd
import json


def main(request, year='2015'):
    #chart1 data
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'by-item_202010305.xls')
    excel_df = pd.read_excel(excel_path, header=4, thousands=',')
    excel_df = excel_df.drop(0)
    excel_df = excel_df.drop([excel_df.columns[3], excel_df.columns[4]], axis=1)
    excel_df = excel_df.sort_values(['기간', '수출금액'], ascending=[True, False]).groupby('기간').head(10)
    result = excel_df.to_json(orient='records')
    dataset1_export = json.loads(result)
    excel_df = excel_df.sort_values(['기간', '수입금액'], ascending=[True, False]).groupby('기간').head(10)
    result = excel_df.to_json(orient='records')
    dataset1_import = json.loads(result)
    excel_df = excel_df.sort_values(['기간', '무역수지'], ascending=[True, False]).groupby('기간').head(10)
    result = excel_df.to_json(orient='records')
    dataset1_tradebalance = json.loads(result)
    #print('1====================================>')
    #print(json.dumps(dataset1_tradebalance, indent=4, ensure_ascii=False))
    
    #chart2 data
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'country_trade.xls')
    excel_df = pd.read_excel(excel_path, header=4, thousands=',')
    excel_df = excel_df.drop(0)
    excel_df = excel_df.drop([excel_df.columns[2], excel_df.columns[4], excel_df.columns[5], excel_df.columns[6]], axis=1)
    excel_df['총수출금액'] = excel_df.groupby(['기간']).수출금액.transform('sum')
    excel_df = excel_df.sort_values(['기간', '수출금액'], ascending=[True, False]).groupby('기간').head(10)
    result = excel_df.to_json(orient='records')
    dataset2 = json.loads(result)
    #print('2====================================>')
    #print(json.dumps(dataset2, indent=4, ensure_ascii=False))
    
    #chart3 data
        #---usa data---->
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'usa_trade.xls')
    excel_df = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df = excel_df.drop(0)
    excel_df = excel_df.drop([excel_df.columns[4]], axis=1)
    excel_df.rename(columns = {'년월':'연도', '총무역금액\n(백만불)':'총무역금액', '한국무역금액\n(백만불)':'한국무역금액', '비중\n(%)':'무역비중', '순위':'무역순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'usa_import.xls')
    excel_df2 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df2 = excel_df2.drop(0)
    excel_df2 = excel_df2.drop([excel_df2.columns[0]], axis=1)
    excel_df2.rename(columns = {'총수입금액\n(백만불)':'총수입금액', '한국수입금액\n(백만불)':'한국수입금액', '비중\n(%)':'수입비중', '순위':'수입순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'usa_export.xls')
    excel_df3 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df3 = excel_df3.drop(0)
    excel_df3 = excel_df3.drop([excel_df3.columns[0]], axis=1)
    excel_df3.rename(columns = {'총수출금액\n(백만불)':'총수출금액', '한국수출금액\n(백만불)':'한국수출금액', '비중\n(%)':'수출비중', '순위':'수출순위'}, inplace = True)
    excel_df = pd.concat([excel_df, excel_df2, excel_df3], axis=1, sort=False)
    excel_df = excel_df.head(5)
    excel_df = excel_df.sort_values(['연도'], ascending=True)
    result = excel_df.to_json(orient='records')
    dataset3_usa = json.loads(result)

        #---china data---->
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'china_trade.xls')
    excel_df = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df = excel_df.drop(0)
    excel_df = excel_df.drop([excel_df.columns[4]], axis=1)
    excel_df.rename(columns = {'년월':'연도', '총무역금액\n(백만불)':'총무역금액', '한국무역금액\n(백만불)':'한국무역금액', '비중\n(%)':'무역비중', '순위':'무역순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'china_import.xls')
    excel_df2 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df2 = excel_df2.drop(0)
    excel_df2 = excel_df2.drop([excel_df2.columns[0]], axis=1)
    excel_df2.rename(columns = {'총수입금액\n(백만불)':'총수입금액', '한국수입금액\n(백만불)':'한국수입금액', '비중\n(%)':'수입비중', '순위':'수입순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'china_export.xls')
    excel_df3 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df3 = excel_df3.drop(0)
    excel_df3 = excel_df3.drop([excel_df3.columns[0]], axis=1)
    excel_df3.rename(columns = {'총수출금액\n(백만불)':'총수출금액', '한국수출금액\n(백만불)':'한국수출금액', '비중\n(%)':'수출비중', '순위':'수출순위'}, inplace = True)
    excel_df = pd.concat([excel_df, excel_df2, excel_df3], axis=1, sort=False)
    excel_df = excel_df.head(5)
    excel_df = excel_df.sort_values(['연도'], ascending=True)
    result = excel_df.to_json(orient='records')
    dataset3_china = json.loads(result)

        #---japan data---->
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'japan_trade.xls')
    excel_df = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df = excel_df.drop(0)
    excel_df = excel_df.drop([excel_df.columns[4]], axis=1)
    excel_df.rename(columns = {'년월':'연도', '총무역금액\n(백만￥)':'총무역금액', '한국무역금액\n(백만￥)':'한국무역금액', '비중\n(%)':'무역비중', '순위':'무역순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'japan_import.xls')
    excel_df2 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df2 = excel_df2.drop(0)
    excel_df2 = excel_df2.drop([excel_df2.columns[0]], axis=1)
    excel_df2.rename(columns = {'총수입금액\n(백만￥)':'총수입금액', '한국수입금액\n(백만￥)':'한국수입금액', '비중\n(%)':'수입비중', '순위':'수입순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'japan_export.xls')
    excel_df3 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df3 = excel_df3.drop(0)
    excel_df3 = excel_df3.drop([excel_df3.columns[0]], axis=1)
    excel_df3.rename(columns = {'총수출금액\n(백만￥)':'총수출금액', '한국수출금액\n(백만￥)':'한국수출금액', '비중\n(%)':'수출비중', '순위':'수출순위'}, inplace = True)
    excel_df = pd.concat([excel_df, excel_df2, excel_df3], axis=1, sort=False)
    excel_df = excel_df.head(5)
    excel_df = excel_df.sort_values(['연도'], ascending=True)
    result = excel_df.to_json(orient='records')
    dataset3_japan = json.loads(result)

        #---eu data---->
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'eu_trade.xls')
    excel_df = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df = excel_df.drop(0)
    excel_df = excel_df.drop([excel_df.columns[4]], axis=1)
    excel_df.rename(columns = {'년월':'연도', '총무역금액\n(백만€)':'총무역금액', '한국무역금액\n(백만€)':'한국무역금액', '비중\n(%)':'무역비중', '순위':'무역순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'eu_import.xls')
    excel_df2 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df2 = excel_df2.drop(0)
    excel_df2 = excel_df2.drop([excel_df2.columns[0]], axis=1)
    excel_df2.rename(columns = {'총수입금액\n(백만€)':'총수입금액', '한국수입금액\n(백만€)':'한국수입금액', '비중\n(%)':'수입비중', '순위':'수입순위'}, inplace = True)
    excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'eu_export.xls')
    excel_df3 = pd.read_excel(excel_path, header=2, thousands=',')
    excel_df3 = excel_df3.drop(0)
    excel_df3 = excel_df3.drop([excel_df3.columns[0]], axis=1)
    excel_df3.rename(columns = {'총수출금액\n(백만€)':'총수출금액', '한국수출금액\n(백만€)':'한국수출금액', '비중\n(%)':'수출비중', '순위':'수출순위'}, inplace = True)
    excel_df = pd.concat([excel_df, excel_df2, excel_df3], axis=1, sort=False)
    excel_df = excel_df.head(5)
    excel_df = excel_df.sort_values(['연도'], ascending=True)
    result = excel_df.to_json(orient='records')
    dataset3_eu = json.loads(result)
    #print('3====================================>')
    #print(json.dumps(dataset3, indent=4, ensure_ascii=False))
    
    #chart4 data
    #chart4 data
    if request.method == "POST":
        year = request.POST['year']
    # excel_path = os.path.join(settings.BASE_DIR, 'excel_files', 'small4.xlsx')
    # excel_df = pd.read_excel(excel_path, header=4, thousands=',')
    # excel_df = excel_df.drop(0)
    # excel_df = excel_df.drop(
    #     [excel_df.columns[4], excel_df.columns[5], excel_df.columns[6]], axis=1)
    # excel_df = excel_df.sort_values(by='수출금액', ascending=False).head(3)
    # result = excel_df.to_json(orient='records')

    dataset4 = json.loads(result)
    im_path = os.path.join(settings.BASE_DIR, 'excel_files', '성질별수입.xls')
    im_df = pd.read_excel(im_path, header=4, thousands=',')
    im_df.drop(0)
    data = im_df.sort_values(['기간', '국가명', '금액', '성질명'], ascending=[
                             True, True, False, False]).groupby(['기간', '국가명']).head(1)
    data['성질명'] = data['성질명'].str.split('.').str[-1]
    data = data.rename(columns={'금액': '금액(USD 1000$)', '중량': '중량(ton)'})

    ex_path = os.path.join(settings.BASE_DIR, 'excel_files', '성질별수출.xls')
    ex_df = pd.read_excel(ex_path, header=4, thousands=',')
    ex_df.drop(0)
    data2 = ex_df.sort_values(['기간', '국가명', '금액', '성질명'], ascending=[
        True, True, False, False]).groupby(['기간', '국가명']).head(1)
    data2['성질명'] = data2['성질명'].str.split('.').str[-1]
    data2 = data2.rename(columns={'금액': '금액(USD 1000$)', '중량': '중량(ton)'})

    years = data['기간'].unique()
    data = data[data['기간'] == year].drop(['기간', '수출입구분'], axis=1)
    years = data2['기간'].unique()
    data2 = data2[data2['기간'] == year].drop(['기간', '수출입구분'], axis=1)

    dataset41 = data.to_html(index=False, justify='center', classes=[
        "table-bordered", "table-striped", "table-hover"])
    dataset42 = data2.to_html(index=False, justify='center', classes=[
                              "table-bordered", "table-striped", "table-hover"])

    #print('4====================================>')
    #print(json.dumps(dataset4, indent=4, ensure_ascii=False))

    return render(request, 'main.html', {'dataset1_export': dataset1_export, 'dataset1_import': dataset1_import, 'dataset1_tradebalance': dataset1_tradebalance, 'dataset2': dataset2, 'dataset3_usa': dataset3_usa, 'dataset3_china': dataset3_china, 'dataset3_japan': dataset3_japan, 'dataset3_eu': dataset3_eu, 'dataset4': dataset4, 'dataset41': dataset41, 'dataset42': dataset42, 'year': years})
   
   
def main1(request):
    headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 RuxitSynthetic/1.0 v7129538413 t38550 ath9b965f92 altpub cvcv=2'}
    url='https://search.daum.net/search?w=tot&DA=23A&rtmaxcoll=NNS&q=%EA%B2%BD%EC%A0%9C%EB%AC%B4%EC%97%AD'
    raw=requests.get(url,headers=headers)
    html = BeautifulSoup(raw.text, "html.parser")
    r_news_link=html.select('.coll_cont ul li a.f_link_b')
    time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    newslist=[]
    print("갱신시각:", time)
    url1='https://search.daum.net/search?nil_suggest=btn&w=news&DA=SBC&cluster=y&q=%EB%AC%B4%EC%97%AD%ED%86%B5%EC%83%81'
    raw1 = requests.get(url1,headers=headers)
    html1 = BeautifulSoup(raw1.text, "html.parser")
    r_news_link1=html1.select('.coll_cont ul li a.f_link_b')
    time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    newslist1=[]
    print("갱신시각:", time)
    url2='https://search.daum.net/search?nil_suggest=btn&w=news&DA=SBC&cluster=y&q=%EB%AC%B4%EC%97%AD%ED%88%AC%EC%9E%90'
    raw2 = requests.get(url2,headers=headers)
    html2 = BeautifulSoup(raw2.text, "html.parser")
    r_news_link2=html2.select('.coll_cont ul li a.f_link_b')
    time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    newslist2=[]
    print("갱신시각:", time)

    for link in r_news_link:
        title=link.text
        hyperlink=link.get('href')
        dic ={'title':title,'hyperlink':hyperlink}
        newslist.append(dic)
        print(dic)
    for link in r_news_link1:
        title=link.text
        hyperlink=link.get('href')
        dic ={'title':title,'hyperlink':hyperlink}
        newslist1.append(dic)
        print(dic)
    for link in r_news_link2:
        title=link.text
        hyperlink=link.get('href')
        dic ={'title':title,'hyperlink':hyperlink}
        newslist2.append(dic)
        print(dic)
    return render(request,'main1.html',{'newslist':newslist,'time':time,'newslist1':newslist1,'newslist2':newslist2})


