import datetime
import re

import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import os


def arrivallandscape():

    from arrival_landscape import pdf_p, txt_p



    fp = open(pdf_p, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()

    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    page_no = 0
    with open(txt_p, 'w') as f:

        for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
            if pageNumber == page_no:
                interpreter.process_page(page)

                data = retstr.getvalue()

                ss1 ='\n\n'+ data.split("\n\nAUTH\n\n")[-1]
                ss = data.split("\nMARKET")[0]
                text_list = []

                if page_no == 0:
                    text_list1 = []
                    text_list1.append(str(ss))

                    f.write(str(text_list1))
                    f.write("\n")

                text_list.append(str(ss1))

                f.write(str(text_list))

                f.write("\n")

                retstr.truncate(0)
                retstr.seek(0)

            page_no += 1
        f.close()
def remainingarivals():
    from remaining_arrivals import pdf_p, txt_p,file

    date=re.findall(r'\d{2}\-\d{2}\-\d+', file)[0].replace('-','/')
    try:
        date=datetime.datetime.strptime(date,'%m/%d/%y').strftime('%m/%d/%Y')
    except:
        date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%m/%d/%Y')

    fp = open(pdf_p, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    print(type(retstr))
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    page_no = 0
    with open(txt_p, 'w') as f:

        for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
            if pageNumber == page_no:
                interpreter.process_page(page)

                data = retstr.getvalue()

                data = data.replace('\n', ' ').replace("       ", ' ')


                text_list = []

                if page_no == 0:

                    spl=f"MARKET {date}"
                    if spl in data:


                        ss = data.split(spl)[0]
                    else:
                        ss = data.split("MARKET ")[0]
                    text_list1 = []
                    text_list1.append(str(ss))

                    f.write(str(text_list1))

                    f.write("\n")

                    spl = f"MARKET {date}"
                    if spl in data:

                        ss1 = data.split(spl)[-1]
                    else:
                        ss1 = data.split("MARKET ")[-1]

                    text_list.append(str(ss1))

                    f.write(str(text_list))

                    f.write("\n")
                else:

                    ss1 = data.split("MARKET ")[-1]

                    text_list.append(str(ss1))

                    f.write(str(text_list))

                    f.write("\n")

                retstr.truncate(0)
                retstr.seek(0)

            page_no += 1
        f.close()

def expectedarrivals(pdf_p,path1,file1):

    fp = open(pdf_p, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()

    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    page_no = 0
    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        if pageNumber == page_no:
            interpreter.process_page(page)

            data = retstr.getvalue()

            with open(fr'{path1}\{file1}{page_no}.txt','wb') as file:
                file.write(data.encode('utf-8'))

            retstr.truncate(0)
            retstr.seek(0)

        page_no += 1

    file.close()


