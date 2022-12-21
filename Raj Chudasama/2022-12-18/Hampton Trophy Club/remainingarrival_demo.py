


import  camelot
import pandas as pd


def demo():

    file = r"G:\Raj\PdfExtractor\Raj Chudasama\2022-12-16\Hampton Trophy Club\remaining arrivals 12-16-22.pdf"
    file = r"G:\Raj\PdfExtractor\Raj Chudasama\2022-12-14\Hampton Inn & Suites Trophy Club\remaining arrivals - 12-14-22.pdf"

    tables = camelot.read_pdf(file, pages='all',encoding="utf-8",flavor='stream', suppress_stdout=False)
    pages=tables.n

    frames=[]

    for i in range(0,pages):
        df=tables[i].df




    result = pd.concat(frames)

    print()

    result.to_excel(r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-16\Home2 Suites by Hilton Fort Worth Northlake\gstlista.xlsx')








if __name__ == '__main__':
    demo()