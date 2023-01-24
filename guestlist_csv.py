import pandas as pd

from utils import logger


def guestlist_csv(file):

    excel_file = file.replace('.csv', '.xlsx')

    df = pd.read_csv(file, encoding='utf-8', header=None)
    df = df.fillna('')
    df = df.iloc[:, 32:38]

    df = df.rename(columns={32: 'ROOM', 33: 'TITLE', 34: 'NAME', 35: 'GUEST ', 36: 'COMPANY NAME', 37:'GROUP'})

    df.to_excel(excel_file, index=False)

