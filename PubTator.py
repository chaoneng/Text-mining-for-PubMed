import requests
from bs4 import BeautifulSoup

import time
import csv

# 重新請求:uri=請求網址,querystring=get參數(可不填),headers=請求頭(可不填)
def requests_restful(restful, url, querystring={}, headers={}):

    if restful == 'post':

        # 定義請求次數
        CONN_TIME = 0

        # , allow_redirects=False
        while True:

            try:

                # 發送get請求
                response = requests.post(url, headers=headers, data=querystring, timeout=60)

                # 判斷Http狀態碼
                if response.status_code == 200:
                    return response

            except requests.exceptions.Timeout:

                '''請求超時'''

                CONN_TIME += 1

                print('請求超時等待10秒後重新請求，第%s次重複請求' % CONN_TIME)

                # # 開啟紀錄記事本
                # f = open('log.train_txt', 'a+', encoding='utf-8')
                #
                # # 紀錄重新連線
                # f.write('####################################################################################' + '\n')
                # f.write('請求超時,時間: ' + str(dt.datetime.now()) + '第%s次重複請求' % CONN_TIME + '\n')
                # f.write('####################################################################################' + '\n')

                # # 關閉
                # f.close()

                time.sleep(10)

            except requests.exceptions.ConnectionError:

                '''請求超時'''

                CONN_TIME += 1

                print('請求超時等待10秒後重新請求，第%s次重複請求' % CONN_TIME)

                # # 開啟紀錄記事本
                # f = open('log.train_txt', 'a+', encoding='utf-8')
                #
                # # 紀錄重新連線
                # f.write('####################################################################################' + '\n')
                # f.write('請求超時,時間: ' + str(dt.datetime.now()) + '第%s次重複請求' % CONN_TIME + '\n')
                # f.write('####################################################################################' + '\n')
                #
                # # 關閉
                # f.close()

                time.sleep(10)

    elif restful == 'get':

        # 定義請求次數
        CONN_TIME = 0

        # , allow_redirects=False
        while True:

            try:

                # 發送get請求
                response = requests.get(url, headers=headers, params=querystring, timeout=60)
                # print(response.status_code)

                # 判斷Http狀態碼
                if response.status_code == 200:

                    return response

            except requests.exceptions.Timeout:

                '''請求超時'''

                CONN_TIME += 1

                print('請求超時等待10秒後重新請求，第%s次重複請求' % CONN_TIME)

                # # 開啟紀錄記事本
                # f = open('log.train_txt', 'a+', encoding='utf-8')
                #
                # # 紀錄重新連線
                # f.write('####################################################################################' + '\n')
                # f.write('請求超時,時間: ' + str(dt.datetime.now()) + '第%s次重複請求' % CONN_TIME + '\n')
                # f.write('####################################################################################' + '\n')

                # # 關閉
                # f.close()

                time.sleep(10)

            except requests.exceptions.ConnectionError:

                '''請求超時'''

                CONN_TIME += 1

                print('請求超時等待10秒後重新請求，第%s次重複請求' % CONN_TIME)


                # # 開啟紀錄記事本
                # f = open('log.train_txt', 'a+', encoding='utf-8')
                #
                # # 紀錄重新連線
                # f.write('####################################################################################' + '\n')
                # f.write('請求超時,時間: ' + str(dt.datetime.now()) + '第%s次重複請求' % CONN_TIME + '\n')
                # f.write('####################################################################################' + '\n')
                #
                # # 關閉
                # f.close()

                time.sleep(10)

Resident_data = open('/Users/charleswang/Downloads/lung_test.tsv', 'w')

csvwriter = csv.writer(Resident_data,delimiter='\t')
# 將表頭寫出
csvwriter.writerow(["PMID", "gene"])
#
inputfile = '/Users/charleswang/Downloads/pubmed_result.txt'
# trigger = ''
# taxonomy = ''
# email = ''
# PubTator_username = ''
# url_Submit = ''

url ='https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Gene/'
headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

fh = open(inputfile)

for pmid in fh:
    pmid=pmid.rstrip('\r\n')

    response = requests_restful(restful='get', url=url + pmid + '/BioC/',headers=headers)

    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    if soup.find('id') is not None:
        pmid = soup.find('id').text

        genelist = []
        for i in soup.find_all('annotation'):
            if i.find('infon', {'key': ("type")}).text == 'Gene':
                genename = i.find('text').text
                genelist.append(genename)

        gene_name = ",".join(genelist)

        print(pmid, gene_name)

    csvwriter.writerows([[pmid, gene_name]])
