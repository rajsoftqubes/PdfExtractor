import datetime

import pandas as pd

from utils import logger


def gstchkin_csv(file):

    excel_file = file.replace('.csv', '.xlsx')
    date=(datetime.datetime.today()+datetime.timedelta(1)).strftime('%m/%d/%Y')
    df=pd.read_csv(file, encoding='utf-8', header=None)
    df=df.fillna('')
    df1 = df.iloc[:, 29:48]

    new=df1[[29,30,43,44,46]].copy()

    new1 = new.rename(columns={29: 'Guest Name', 30: 'Hilton Honor Tier',43:'Rate', 44:'Rate Plan', 46:'Room Type'})

    new1['Company']=''
    new1['Arrival Date']=date

    new1=new1[['Guest Name', 'Hilton Honor Tier', 'Company', 'Rate', 'Rate Plan', 'Arrival Date', 'Room Type']]

    new1.to_excel(excel_file, index=False)
