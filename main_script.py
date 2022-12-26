import datetime
import os
import glob
from expected_arrivals import expected_arrivals
from inhouse_guestlist import inhouseguests
from arrivallanscape_new import arrival_landscape
from guest_list import guest_list
from remainingarrivals_df import remaining_arrivals


for i in range(0, 1):

    today_date=(datetime.datetime.today()-datetime.timedelta(i)).strftime('%Y-%m-%d')

    cwd = os.getcwd()

    path1=cwd+'\\Raj Chudasama\\'+today_date

    arr = os.listdir(path1)

    for dir1 in arr:

        path2=path1+'\\'+dir1

        for file_path in glob.glob(path2+'\\*.pdf'):

            file_name = os.path.basename(file_path)

            if file_name.startswith('EXPECTED ARRIVALS'):
                expected_arrivals(file_path, path2,file_name)
                print('Expected Arrivals generated...', today_date)

            if file_name.startswith('IN HOUSE'):
                inhouseguests(file_path,path2)
                print('In House guest list generated...', today_date)

            if file_name.startswith(('guest','gstlist')):
                guest_list(file_path)
                print('Guest List generated...', today_date)

            if file_name.startswith('arrivalllandscape'):
                arrival_landscape(file_path)
                print('Arrivals Landscape generated...', today_date)

            if file_name.startswith('remaining'):
                remaining_arrivals(file_path)
                print('Remining Arrivals generated...', today_date)

            for zippath in glob.iglob(os.path.join(path2, '*.txt')):
                os.remove(zippath)

            # for zippath in glob.iglob(os.path.join(path2, '*.xlsx')):
            #     os.remove(zippath)
