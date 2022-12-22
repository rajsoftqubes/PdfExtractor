import datetime
import re
import pdfplumber
import pandas as pd


def demo():

    pdf = pdfplumber.open(r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-09\Hampton Trophy Club\remaining arrivals.pdf')

    page = pdf.pages

    data_list=[]

    for p in page:
        text = p.extract_text()

        data=text.split('MARKET ')[1]

        data=data.splitlines()

        for index,d in enumerate(data):


            if '/' in d:

                name=re.findall(r'(.*?)\w{1}\s+\-\s+',d)
                if name==[]:
                    name=re.findall(r'(.*?)\s{3}\w{1}\s+\w{1}',d)

                if name:
                    name=name[0]

                    tier=re.findall(r'(\w{1})(\s{1}\-\s+\d{9})',d)
                    if tier:
                        tier=tier[0][0]
                    else:
                        tier=''

                    rt = re.findall(r'([A-Z]\s{1}[A-Z]\s{1}\d{3}\s+\w{3,})',d)
                    if rt==[]:
                        rt=re.findall(r'([A-Z]\s{1}[A-Z]\s{1}\w{3,})',d)
                    if rt:
                        room_type=rt[0].split(' ')[-1]

                    d1=data[index+1]

                    com=re.findall(r'(.*?)\d{8}',d1)
                    if com:
                        com=com[0]

                    price=re.findall(r'(\$\d+\.\d+)',d1)
                    if price:
                        price=price[0]

                    rate_plan=d1.split(' ')[-1]

                    data_dict={
                        'Guest Name':name,
                        'Hilton Honor Tier':tier,
                        'Company':com,
                        'Rate':price,
                        'Rate Plan':rate_plan,
                        'Arrival Date':datetime.datetime.today().strftime('%m/%d/%Y'),
                        'Room Type':room_type
                    }

                    data_list.append(data_dict)

                    print(data_dict)

        # data=text.split('AUTH')[-1]

        # df = pd.read_csv(StringIO(data), on_bad_lines='skip', sep="\\n",header=None,engine='python')
        #
        # main_df_list=[]
        #
        # for d, d1 in df.iterrows():
        #     d2=d1[0]
        #     df1 = pd.read_csv(StringIO(d2), on_bad_lines='skip', sep=" ", header=None,engine='python')
        #     main_df_list.append(df1)
        #
        # df_merge = pd.concat(main_df_list, ignore_index=True)
        # df_merge=df_merge.fillna('')
        # df_merge=df_merge.astype(str)
        #
        # for rownum, rowdata in df_merge.iterrows():
        #
        #     fd=rowdata[0]
        #
        #     dt=is_date(fd)
        #
        #     if '/' in fd and dt ==False:
        #         name = fd
        #
        #         tier=df_merge.iloc[rownum,1]
        #
        #         con_name = df_merge.iloc[rownum + 1, 0]
        #         if con_name.isdigit() == True:
        #             con_name = ''
        #
        #         price=df_merge.iloc[rownum+1,2]
        #         if price=='':
        #             price=df_merge.iloc[rownum+1,1]
        #
        #         rate_plan=df_merge.iloc[rownum+1,6]
        #         if rate_plan=='':
        #             rate_plan = df_merge.iloc[rownum + 1, 5]
        #
        #         rt=[]
        #         for i in range(5,9):
        #
        #             roomt=df_merge.iloc[rownum,i]
        #             rt.append(roomt)
        #
        #         for j in rt:
        #             if '.' in j:
        #                 j=j.split('.')[0]
        #             if j.isdigit()==False and len(j)>=3:
        #                 room_type=j
        #                 break
        #
        #         data_dict={
        #             'Guest Name':name,
        #             'Hilton Honor Tier':tier,
        #             'Company':con_name,
        #             'Rate':price,
        #             'Rate Plan':rate_plan,
        #             'Arrival Date':datetime.datetime.today().strftime('%m/%d/%Y'),
        #             'Room Type':room_type
        #         }
        #         data_list.append(data_dict)

    df = pd.DataFrame(data_list)
    df.to_excel(r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-09\Hampton Trophy Club\remaining arrivals.xlsx')


if __name__ == '__main__':
    demo()