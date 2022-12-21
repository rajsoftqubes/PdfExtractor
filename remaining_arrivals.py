import re

import tabula
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import os
import pandas as pd
file='remaining arrivals 12-19-22'

txt_p = r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-19\Hampton Trophy Club\remaining arrivals 12-19-22.txt'
excel_p = r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-19\Hampton Trophy Club\remaining arrivals 12-19-22.xlsx'
pdf_p = r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-19\Hampton Trophy Club\remaining arrivals 12-19-22.pdf'


def demo():


    from pdf_to_txt import remainingarivals

    remainingarivals()

    with open(txt_p, 'r') as f:
        data = f.readlines()

    data_list = []

    for index, d in enumerate(data):

        main12 = ''.join(d).replace('\\n', ' ')
        # main=d
        if index == 0:
            try:
                arrivaldate = re.findall(r'ARRIVALS FOR (\d{2}\/\d{1}\/\d{4})', main12)[0]
            except:

                arrivaldate = re.findall(r'ARRIVALS FOR (\d{2}\/\d{2}\/\d{4})', main12)[0]


        else:
            main=d

            # main1 = d.replace('*','').replace('-',' ').replace("['","[' ")
            names = []

            namess = re.findall(r'(((\s{1}\w+))+\/((\w+\s{1}))+)', main)

            for i2 in namess:
                for i3 in i2:
                    i21 = i3.split('/')[-1]
                    try:

                        i22 = int(i21)
                    except:
                        i22 = ''
                    if '/' in i3 and i22 == '' and i3 not in names:
                        names.append(i3)


            # main = ''.join(d).replace('\\n', ' ')
            column_list=[]

            rpcodess = re.findall('(\$\d+\.\d+\s+\$\d+\.\d+\s+)((\w+\-\w+)|(\w+))', main)
            rpcodes = [j[1] for j in rpcodess]
            n11 = names
            alen = len(n11)
            z=0

            for index, j in enumerate(n11):
                z+=1
                colum_dict = {}
                j1=j.split('/')[-1]

                namelen=len(re.findall(j,main))
                if namelen==0:
                    namelen=len(re.findall(j1,main))



                if namelen>1:
                    ad1=main.split(j)
                    ad1.pop(0)
                    for d1 in ad1:


                        if index <alen:
                            try:
                                if n11[index+1] not in d1:
                                    colum_dict[j] = d1
                                    column_list.append(colum_dict)
                                else:
                                    d1=d1.split(n11[index+1])[0]
                                    colum_dict[j] = d1
                                    column_list.append(colum_dict)
                            except:
                                if alen - 1 == index:

                                    colum_dict[j] = d1
                                    column_list.append(colum_dict)
                        else:
                            d1 = d1.split(n11[index + 1])[0]
                            colum_dict[j] = d1
                            column_list.append(colum_dict)

                else:


                    ad = main.split(j)

                    try:
                        ad1 = ad[1].split(n11[index+1])
                        colum_dict[j] = ad1[0]
                        column_list.append(colum_dict)
                    except Exception as e:
                        if alen - 1 == index:
                            ad1 = ad[1]
                            colum_dict[j] = ad1
                            column_list.append(colum_dict)



            # for index,j in enumerate(n11):
            #
            #     if index == 0:
            #
            #         ad = main.split(j[1:])
            #         column_list.append(ad)
            #         if len(n11) == 1:
            #             ad = main.split(j)[1]
            #             column_list.append(ad)
            #     elif index < alen:
            #         try:
            #
            #             ad = main.split(j)
            #         except:
            #             ad = ''
            #         if ad:
            #             column_list.append(ad)
            #             if index == (alen - 1):
            #                 ad = main.split(j)[1]
            #                 column_list.append(ad)
            c=0
            for columnn in column_list:

                for name, colum in columnn.items():
                    colum = colum.replace('\\n', ' ')

                    name = name 
                    print(name)

                    num = re.findall(r'( \w{1} - \d+)', colum)
                    if num:
                        num = num[0].split('-')[0]
                    else:
                        num = ''

                    try:

                        price = re.findall(r'(\$\d+\.\d+)', colum)
                        for p in price:
                            p = p.replace('$', '')
                            if p == '0.00':
                                price = price[1]
                                break
                            else:
                                price = price[0]
                                break
                    except:
                        price = ''
                    if price == []:
                        price = ''

                    rp = re.findall('(\$\d+\.\d+\s+)(\w{1}\-\w{3})', colum)
                    if not rp:
                        rp = re.findall('(\w{1}\-\w{3})', colum)

                    if not rp:
                        rp = re.findall('(\$\d+\.\d+)\)(\s+\w{1}\-\w{3})', colum)
                    if not rp:
                        rp = re.findall(r'(\$\d+\.\d+\s+) (\w{3})', colum)
                    if not rp:
                        rp = re.findall(r'(\s+)(\w{1} \w{3})', colum)

                    if rp and type(rp)==list:
                        rp = rp[0][-1].strip().replace(' ','-')

                    # com = re.findall(r'(\$\d+\.\d+ [A-Z]{1}-\w{3})(.*?)(\$\d+\.\d+)|(\$\d+\.\d+\s+(.*?)\d{8})|(\w{2}\s+)(\w+\s+)(\d{8})',colum)

                    columm=colum.replace(',','').replace('.','')
                    com = re.findall(r'(((\s{1}\w+))+)(\s{2}\d{8})',columm)
                    # com = re.findall(r'(CC\s{2}(.*?)\s{2}\d{8})',columm)
                    if com:
                        cname = com[0][0].strip()
                        try:
                            c2=int(cname)
                            if c2:
                                c2=True

                        except:
                            c2=cname
                        if 'BEST AVAILABLE RATE' in cname or 'DISCOUNTS' in cname or cname=='CC' or cname=='IN' or cname in rp or c2==True or cname=='FP':
                            cname = ''
                    else:
                        cname = ''

                    rt = re.findall(r'(\d{8}\s+)(\w{3})(\s+\w{2})', colum)

                    if not rt:
                        rt = re.findall(r'(\d{8}\s+)(\w{5})(\s+\w{2})', colum)

                    if not rt:
                        rt = re.findall(r'(\d{8}\s+)(\w{4})(\s+\w{2})', colum)
                    if not rt:
                        rt = re.findall(r'(\d{8}\s+)(\w{3})', colum)
                    if not rt:
                        rt = re.findall(r'(\d{8}\s+)(\w{4})', colum)
                    if not rt:
                        rt = re.findall(r'(\d{8}\s+)(\w{5})', colum)

                    if not rt:
                        rt = re.findall(r'(\w{1}\s+\w{1}\s+\d{3}\s+)(\w{5})', colum)
                    if not rt:
                        rt = re.findall(r'(\w{1}\s+\w{1}\s+\d{3}\s+)(\w{4})', colum)
                    if not rt:
                        rt = re.findall(r'(\w{1}\s+\w{1}\s+\d{3}\s+)(\w{3})', colum)

                    if not rt:
                        rt = re.findall(r'(\w{1}\s+\w{1}\s+)(\w{5})', colum)
                    if not rt:
                        rt = re.findall(r'(\w{1}\s+\w{1}\s+)(\w{4})', colum)
                    if not rt:
                        rt = re.findall(r'(\w{1}\s+\w{1}\s+)(\w{3})', colum)

                    # if not rt:
                    #     rt=re.findall(r'(\w{5})(\d{1}\,\d{1} [A-Z][A-Z])',colum)
                    # if not rt:
                    #     rt=re.findall(r'(\w{3})(\d{1}\,\d{1} [A-Z][A-Z])',colum)
                    # if not rt:
                    #     rt=re.findall(r'(\w{3}) (\d{1}\,\d{1} [A-Z][A-Z])',colum)
                    # if not rt:
                    #     rt = re.findall(r'(\w{5}) (\d{1}\,\d{1} [A-Z][A-Z])', colum)
                    if rt:
                        romtype = rt[0][1]
                    else:
                        romtype = ''

                    mian_dict = {
                        'Guest Name': name,
                        'Hilton Honor Tier': num,
                        'Company': cname,
                        'Rate': price,
                        'Rate Plan': rp,
                        'Arrival Date': arrivaldate,
                        'Depart Date': '',
                        'Room Type': romtype
                    }
                    c+=1
                    if rp:
                        data_list.append(mian_dict)
                        print(mian_dict)


    df = pd.DataFrame(data_list)

    df.to_excel(excel_p, index=False)


if __name__ == '__main__':
    demo()