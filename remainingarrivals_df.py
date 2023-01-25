import datetime
import re
import pdfplumber
import pandas as pd

from utils import logger


def remaining_arrivals(file):

    try:

        excel_file = file.replace('.pdf', '.xlsx')

        pdf = pdfplumber.open(file)

        page = pdf.pages

        data_list = []

        for p in page:
            text = p.extract_text()

            data = text.split('MARKET ')[1]

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

                        rt = re.findall(r'([A-Z]\s{1}[A-Z]\s{1}\d{3}\s+\w{3,})', d)
                        if rt == []:
                            rt = re.findall(r'([A-Z]\s{1}[A-Z]\s{1}\w{3,})', d)
                        if rt:
                            room_type = rt[0].split(' ')[-1]

                        d1 = data[index + 1]

                        com = re.findall(r'(.*?)\d{8}', d1)
                        if com:
                            com = com[0]

                        price = re.findall(r'(\$\d+\.\d+)', d1)
                        if price:
                            price = price[0]

                        rate_plan = d1.split(' ')[-1]

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
