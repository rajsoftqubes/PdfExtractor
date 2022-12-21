import camelot
import pandas as pd
import datetime

def demo():

    file = r"G:\Raj\PdfExtractor\Raj Chudasama\2022-12-20\Hampton Trophy Club\remaining arrivals 12-20-22.pdf"

    tables = camelot.read_pdf(file, pages='all',encoding="utf-8",flavor='stream', suppress_stdout=False)
    pages=tables.n

    data_list=[]

    for i in range(0,pages):
        df=tables[i].df

        for rownum, rowdata in df.iterrows():



            if '\n' in rowdata[0] and 'TIME' not in rowdata[0]:


                df[[0, 1]] = df[0].str.split('\n', 1, expand=True)
                df = df.fillna('')
                break
            elif 'COMPANY NAME' in rowdata[0]:
                df = df.drop(df.index[0:rownum+2])
                break

        if i==0:
            df=df.drop(labels=0)
        else:
            df=df

        df=df.reset_index(drop=True)

        for rownum, rowdata in df.iterrows():

            for row in rowdata:


                if '/' in row:


                    name=row

                    con_name=df.iloc[rownum+1,0]

                    tier=df.iloc[rownum, 1]
                    if tier:
                        tier=tier.split('-')[0]

                    roomtype=[]
                    rt1=df.iloc[rownum,4]
                    rt2=df.iloc[rownum,5]
                    rt3=df.iloc[rownum,6]
                    roomtype.append(rt1)
                    roomtype.append(rt2)
                    roomtype.append(rt3)

                    for r in roomtype:
                        if r=='':
                            pass
                        elif r.isdigit()==True:
                            pass
                        elif len(r)>=3 and r.isdigit()==False:
                            room_type=r



                    rate_plan=df.iloc[rownum+1,-1]
                    if '\n' in rate_plan:

                        rate_plan=rate_plan.split('\n')[0]

                    price=df.iloc[rownum+1,-2]

                    if price =='$0.00':
                        price = df.iloc[rownum + 1, -3]
                    elif price=='':
                        price=df.iloc[rownum+1,-1].split('\n')[1]

                    mian_dict = {
                        'Guest Name': name,
                        'Hilton Honor Tier': tier,
                        'Company': con_name,
                        'Rate': price,
                        'Rate Plan': rate_plan,
                        'Arrival Date': datetime.datetime.today().strftime('%m/%d/%Y'),
                        'Depart Date': '',
                        'Room Type': room_type
                    }

                    print(mian_dict)

                    data_list.append(mian_dict)
    #

    df = pd.DataFrame(data_list)
    df.to_excel(r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-20\Hampton Trophy Club\remaining arrivals 12-20-22.xlsx')


if __name__ == '__main__':
    demo()