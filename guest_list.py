import camelot
import pandas as pd
import warnings

from utils import logger


warnings.simplefilter(action='ignore', category=FutureWarning)


def guest_list(file):

    try:

        excel_file = file.replace('.pdf', '.xlsx')

        tables = camelot.read_pdf(file, pages='all', encoding="utf-8", flavor='stream', suppress_stdout=False)
        pages = tables.n

        frames = []

        for i in range(0, pages):
            df = tables[i].df

            try:

                for index, row in df.iterrows():
                    value = row[0]

                    if 'ROOM\nTITLE' not in value and 'ROOM' not in value:
                        df = df.drop(labels=index)

                    else:

                        df.rename(columns=df.iloc[0], inplace=True)

                        if 'ROOM\nTITLE' in df.columns[0]:

                            df[['ROOM', 'TITLE']] = df['ROOM\nTITLE'].str.split('\n', 1, expand=True)
                            df = df.fillna('')
                            df.pop('ROOM\nTITLE')
                            df = df.drop(df.index[0:3])

                            df = df[['ROOM', 'TITLE', 'NAME', 'GUEST', 'COMPANY NAME', 'GROUP']]
                        elif 'ROOM' in df.columns[0]:

                            df = df.drop(df.index[0:3])

                        df = df[['ROOM', 'TITLE', 'NAME', 'GUEST', 'COMPANY NAME', 'GROUP']]
                        frames.append(df)

                        break

            except Exception as e:
                logger.debug(e)

        result = pd.concat(frames)
        result.to_excel(excel_file, index=False)


    except Exception as e:

        logger.debug(e)

