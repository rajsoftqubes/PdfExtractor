import re
import pdfplumber
import pandas as pd
from utils import logger



def expected_arrivals(file):

    try:
        excel_file = file.replace('.pdf', '.xlsx')

        pdf = pdfplumber.open(file)

        page = pdf.pages

        data_list = []

        for p in page:
            text = p.extract_text()

            data = text.splitlines()

            for index, d in enumerate(data):

                code = re.findall(r'(\w{2}\s+\@\d{5})', d)

                if code:

                    roomtype = code[0].split()[0]

                    name = re.findall(r'(\w+\,\s+\w+)|(\w+\-\w+\,\s+\w+)', d)

                    for n in name[0]:
                        if n == '':
                            pass
                        else:
                            name = n
                            break

                    groupcode = re.findall(r'(\w{2}\d{4})', d)
                    if groupcode:
                        groupcode = groupcode[0]
                    else:
                        groupcode = ''

                    departdate = re.findall(r'(\d{2}\-\w{3}\-\d{2})', d)
                    if departdate:
                        departdate = departdate[0]
                    else:
                        departdate = ''

                    rateplan = re.findall(r'(\d{2}\-\w{3}\-\d{2}\s+)(\w+)', d)
                    if rateplan:
                        rateplan = rateplan[0][-1]
                    else:
                        rateplan = ''

                    d1 = data[index + 1]

                    price = re.findall(r'(\d+\.\d+)', d1)
                    if price:
                        price = price[0]
                    else:
                        price = ''

                    m1 = re.findall(r'(\d{8})', d1)[0]
                    com = d1.split(m1)[-1]

                    company = re.findall(r'(.*?)(\d{2}\:\d{2})', com)
                    if company:
                        company = company[0][0]
                    else:

                        company = re.findall(r'(.*?)(\d+\.\d+)', com)
                        if company:
                            company = company[0][0]

                    d2 = data[index + 2]

                    arrivaldate = re.findall(r'(\d{2}\-\w{3}\-\d{2})', d2)
                    if arrivaldate:
                        arrivaldate = arrivaldate[0]
                    else:
                        arrivaldate = ''

                    q1 = re.findall(r'(\d{2}\-\w{3}\-\d{2})(\s\w+)', d2)
                    if q1:

                        q3 = q1[0][-1].strip()
                        if len(q3) > 5:
                            ocn = q3
                            company = company + ' ' + ocn

                    data_dict = {
                        'Guest Name': name,
                        'Group Code': groupcode,
                        'Company': company,
                        'Rate': price,
                        'Rate Plan': rateplan,
                        'Arrival Date': arrivaldate,
                        'Depart date': departdate,
                        'Room Type': roomtype
                    }

                    data_list.append(data_dict)

        df = pd.DataFrame(data_list)
        df.to_excel(excel_file, index=False)

    except Exception as e:

        logger.debug(e)
