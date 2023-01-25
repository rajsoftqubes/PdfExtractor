import datetime
import re
from utils import logger

import pandas as pd
import pdfplumber


def arrival_landscape_new(file):

    excel_file = file.replace('.pdf', '.xlsx')



    try:

        pdf = pdfplumber.open(file)

        page = pdf.pages

        data_list = []

        for p in page:
            text = p.extract_text()

            data = text.split('AUTH')[-1]
            if '/' not in data:
                data=text.split('AUTH')[-2]

            data = data.splitlines()

            for index, d in enumerate(data):

                if '/' in d:

                    name = re.findall(r'(.*?)\w{1}\s+\-\s+', d)
                    if name == []:
                        name = re.findall(r'(.*?)\s{3}\w{1}\s+\w{1}', d)

                    if name:
                        name = name[0]

                        tier = re.findall(r'(\w{1})(\s{1}\-\s+\d{9})', d)
                        if tier:
                            tier = tier[0][0]
                        else:
                            tier = ''

                        price = re.findall(r'(\$\d+\.\d+)', d)
                        if price:
                            price = price[0]
                        else:
                            price = ''

                        rate_plan = d.split(' ')[-1]

                        d1 = data[index + 1]

                        rt = re.findall(r'(\d{8}\s+\w{3,})', d1)
                        if rt:
                            room_type = rt[0].split(' ')[-1]
                        else:
                            room_type = ''

                        com = re.findall(r'(.*?)\d{8}', d1)
                        if com:
                            com = com[0]

                        data_dict = {
                            'Guest Name': name,
                            'Hilton Honor Tier': tier,
                            'Company': com,
                            'Rate': price,
                            'Rate Plan': rate_plan,
                            'Arrival Date': datetime.datetime.today().strftime('%m/%d/%Y'),
                            'Room Type': room_type
                        }

                        data_list.append(data_dict)

        df = pd.DataFrame(data_list)
        df.to_excel(excel_file, index=False)


    except Exception as e:

        logger.debug(e)

#
# file=r'G:\Raj\PdfExtractor\Raj Chudasama\2023-01-24\Home2 Suites by Hilton Dallas Grand Prairie\arrivalllandscape_letter.pdf'
# arrival_landscape_new(file)