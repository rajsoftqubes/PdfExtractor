import  camelot
import pandas as pd


def demo():

    file = r"G:\Raj\PdfExtractor\Raj Chudasama\2022-12-20\Hampton Trophy Club\guest all list 12-20-22.pdf"

    tables = camelot.read_pdf(file, pages='all',encoding="utf-8",flavor='stream', suppress_stdout=False)
    pages=tables.n

    frames=[]

    for i in range(0,pages):
        df=tables[i].df

        try:

            for index, row in df.iterrows():
                value = row[0]
                if '\n' in value:

                    df.rename(columns=df.iloc[0], inplace = True)
                    df = df.drop(labels=[index,index+1])

                    if 'ROOM\nTITLE' in df.columns[0]:

                        df[['ROOM', 'TITLE']] = df['ROOM\nTITLE'].str.split('\n',1,expand=True)
                        df=df.fillna('')
                        df.pop('ROOM\nTITLE')

                        df=df[['ROOM', 'TITLE', 'NAME','GUEST', 'COMPANY NAME', 'GROUP']]

                    df = df[['ROOM', 'TITLE', 'NAME', 'GUEST', 'COMPANY NAME', 'GROUP']]
                    frames.append(df)

                    break

                else:
                    df = df.drop(labels=index)
        except Exception as e:
            df=''



    result = pd.concat(frames)

    print()

    result.to_excel(r'G:\Raj\PdfExtractor\Raj Chudasama\2022-12-20\Hampton Trophy Club\guest all list 12-20-22.xlsx')








if __name__ == '__main__':
    demo()