import datetime
import re
import pdfplumber
import pandas as pd


def inhouseguests(file,path):

    excel_file=file.replace('.pdf','.xlsx')

    pdf = pdfplumber.open(file)

    page = pdf.pages

    data_list=[]

    for p in page:
        text = p.extract_text()

        data = text.splitlines()

        for index, d in enumerate(data):

            roomnum=re.findall(r'(^\d{3}\s+)',d)

            if roomnum:



                d1 = data[index + 1].split()

                if len(d1)==1:
                    name = re.findall(r'(\w+\,\s+\w+)', d)[0]
                    guest_name=name
                else:
                    try:
                        name = re.findall(r'(\w+\,)', d)[0]
                        guest_name=f'{name}{d1[-1]}'
                    except:

                        name=d1[-1]
                        gt11=re.findall(r'\@[A-Z]',d)[0]
                        gt12=d.split(gt11)
                        d=f'{gt12[0]}  {gt11} {name} {gt12[-1]}'

                d2=d.split(name)

                d3=d2[0].split()



                roomnum=d3[0]
                room_type=d3[1]
                room_stat=d3[2]
                gt=d3[3]

                m4=d2[-1]

                dates=' '.join(re.findall(r'(\d{2}\-\w{3}\-\d{2})',m4))

                m41=m4.split(dates)[0]

                code1=re.findall(r'[A-Z]\s{1}',m41)
                if code1:
                    code=code1[0]
                    company = m41.split(code)[-1]
                else:
                    code=''
                    company=m41

                arrivaldate=dates.split(' ')[0]
                deprtdate=dates.split(' ')[-1]
                p1=deprtdate+r'(.*?)\s+\d{1}'

                city=re.findall(p1,m4, re.IGNORECASE)
                if city:
                    city=city[0]
                else:
                    city=''


                main_dict={

                    'Room Num':roomnum,
                    'Room Type':room_type,
                    'Room Status':room_stat,
                    'GT':gt,
                    'Guest/RoomMate':guest_name,
                    'MBV Level':code,
                    'Company':company,
                    'ArrivalDate':arrivaldate,
                    'DepartDate':deprtdate,
                    'City':city,
                }
                data_list.append(main_dict)

    df = pd.DataFrame(data_list)
    df.to_excel(excel_file, index=False)


if __name__ == '__main__':
    inhouseguests()