import re

import tabula
import pandas as pd
from pdf_to_txt import expectedarrivals


def expected_arrivals(file, path, file_name):
    excel_p = file.replace('.pdf', '.xlsx')
    pdf_p = file
    path1 = path
    file1 = file_name.replace('.pdf', '')

    expectedarrivals(pdf_p, path1, file1)

    df = tabula.read_pdf(pdf_p, pages='all', silent=True)

    all_data = []
    x = 0

    for d in df:

        d = d.fillna('')

        columns = d.columns.to_list()

        for rownum, rowdata in d.iterrows():

            for columnnum, column in enumerate(columns):

                if rowdata[column]:
                    a1 = len(rowdata[column].split(' '))

                try:
                    asd1 = re.findall(r'\@\d{5}', rowdata[column])[0]
                except:
                    asd1 = ''

                if asd1 and a1 <= 3:

                    try:

                        roomtype = d.iloc[rownum, columnnum - 1]
                        if not roomtype:
                            roomtype = rowdata[column].split(' ')[0]
                        if int(roomtype):
                            roomtype = rowdata[column].split(' ')[0]

                        if not roomtype:
                            roomtype = rowdata[column].split(' ')[0]
                    except Exception as e:
                        if roomtype == '':

                            roomtype = d.iloc[rownum, columnnum - 1]
                        else:
                            roomtype = roomtype

                    rt = re.findall(r'\d+(?:,\d*)?', roomtype)
                    if rt:
                        roomtype = roomtype.split(rt[0])[-1]

                    try:
                        arrivaldate = d.iloc[rownum + 2, columnnum]
                    except Exception as e:
                        arrivaldate = ''

                    try:
                        guestname = d.iloc[rownum, d.columns.get_loc('Unnamed: 0')]
                        if not guestname:
                            guestname = d.iloc[rownum, d.columns.get_loc("GT Guest Name/ MARSHA#/")]
                    except Exception as e:

                        guestname = d.iloc[rownum, d.columns.get_loc("GT Guest Name/ MARSHA#/")]
                    try:

                        guestname = re.findall(r'(\w+\, \w+\s\w+)', guestname)[0]
                    except:

                        guestname = re.findall(r'(\w+\, \w+)', guestname)[0]

                    groupcode = d.iloc[rownum, d.columns.get_loc("Group Code/")]

                    exc_date = d.iloc[rownum, d.columns.get_loc("Exp Dep")]
                    try:

                        comname = d.iloc[rownum + 1, d.columns.get_loc("Group Code/")]
                    except:
                        comname = ''

                    rate_plan = d.iloc[rownum, d.columns.get_loc("R + Plan/Excx")]
                    try:
                        rate = d.iloc[rownum + 1, d.columns.get_loc("R + Plan/Excx")]
                    except:
                        rate = ''

                    codes = d.iloc[rownum, columnnum].split('@')[-1]

                    if roomtype == '':
                        roomtype = d.iloc[rownum, columnnum].split(' ')[0]

                    if arrivaldate == '':

                        with open(rf'{path1}\{file1}{x}.txt', 'r') as f:
                            data = f.read()

                        data = data.replace('\n', ' ')

                        d1 = []

                        arrialdates = re.findall(r'(\@\d{5}  \d{1} \/ \d{2})( \d{2}\-\w{3}\-\d{2})|(\@\d{5} \/ )( \d{2}\-\w{3}\-\d{2})|(\@\d{5}  \d{1} \/ \d{1})( \d{2}\-\w{3}\-\d{2})',data)

                        if arrialdates:

                            for i in arrialdates:
                                for j1 in i:
                                    if '-' in j1:
                                        d1.append(j1)

                            d12 = d1[-1]
                            arrivaldate = d12
                        else:
                            data1 = data.split(codes)[1].split(guestname)[0]

                            arrivaldate = re.findall(r'\d{2}\-\w{3}\-\d{2}', data1)[0]
                    #
                    data_dict = {
                        'Guest Name': guestname,
                        'Group Code': groupcode,
                        'Company': comname,
                        'Rate': rate,
                        'Rate Plan': rate_plan,
                        'Arrival Date': arrivaldate,
                        'Depart date': exc_date,
                        'Room Type': roomtype,
                        'code': codes
                    }

                    all_data.append(data_dict)

        x += 1

    df1 = pd.DataFrame(all_data)

    df1.to_excel(excel_p, index=False)

    result_df = pd.read_excel(excel_p)
    result_df = result_df.fillna('')
    for ii in range(0, len(df)):

        with open(fr'{path1}\{file1}{ii}.txt', 'r') as f:
            data = f.read()

        data = data.replace('\n', ' ')

        prices = re.findall(r'(\d+\.\d{2})', data)

        codes = re.findall(r'(\@\d+)', data)

        for c1 in codes:
            c2 = c1.replace('@', '')
            c3 = result_df['code'].isin([int(c2)]).any()

            if c3 == False:
                codes.remove(c1)

        df3 = result_df[result_df['Rate'] == '']
        for d in df3['code']:

            for code, p in zip(codes, prices):

                code = code.strip().replace('@', '')

                if int(code) == d:
                    sqlRun = result_df.query(f"code == {d} ")['code']
                    # 2 : Got sql output e.g. 110,000
                    # 3
                    result_df.loc[sqlRun.index, "Rate"] = p

    result_df.pop('code')

    result_df.to_excel(excel_p)


if __name__ == '__main__':
    expected_arrivals()
