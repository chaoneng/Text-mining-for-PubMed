import csv
import pandas as pd
import numpy as np
import re
import os

def strB2Q(ustring):
    """把字符串半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            rstring += uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        rstring += chr(inside_code)
    return rstring

def strQ2B(ustring):

    rstring = ""

    for uchar in ustring:
        inside_code = ord(uchar)

        if inside_code == 12288:
            inside_code = 32

        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248

        rstring += chr(inside_code)

    return rstring

gene_data = open('/Users/charleswang/Downloads/gene_data_CN.tsv', 'w')

csvwriter = csv.writer(gene_data,delimiter='\t')
# 將表頭寫出
csvwriter.writerow(["data,gene_name"])

# 讀gene_name資料表
data_gene = pd.read_csv('/Users/charleswang/Downloads/co/Gene_Name.tsv',header=None)
gene = data_gene[0].values

# 讀co_interactoions資料表
data = pd.read_csv('/Users/charleswang/Downloads/co/co_interactoions_CN.csv',header=None)

# 將co_interactoions_CN讀出
for txt_data in data.values:
    txt_list = []

    # 將co_interactoions_CN 第0欄及第1欄取出,放進list
    txt_list.append(txt_data[0])
    txt_list.append(txt_data[1])

    # 將list轉為str
    txt_name = ",".join(txt_list)

    # 將gene_name資料表讀出
    for gene_name in gene:
        # 進行比對只要比對中其一即可寫入
        if re.search(r'\b' + strB2Q(str(gene_name)) + r'\b', strB2Q(str(txt_list[0]))) or re.search(r'\b' + strB2Q(str(gene_name)) + r'\b', strB2Q(str(txt_list[1]))):
            print(txt_name,gene_name)

            csvwriter.writerows([[txt_name, gene_name]])

