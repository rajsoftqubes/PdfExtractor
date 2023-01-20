import email
import imaplib
import json
import re
import datetime
import os
import glob
from expected_arrivals_new import expected_arrivals
from inhouse_guestlist import inhouseguests
from arrivallanscape_new import arrival_landscape_new
from guest_list import guest_list
from remainingarrivals_df import remaining_arrivals


def email_automation():
    with open('property.json', 'r') as myfile:
        data = myfile.read()

    obj = json.loads(data)

    dir_name = "."
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".pdf"):
            os.remove(os.path.join(dir_name, item))
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login("no-reply@kriyahotels.com", "dxzxiglcpynssoqd")
    print("logged in!!")
    asd=mail.select("Guestlist")
    print(asd)

    type, data = mail.search(None, 'UNSEEN')

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        sender_mail = re.findall(r'(\w+\-sales\@kriyahotels.com)', raw_email_string)

        for s in sender_mail:
            property_name = obj[s]
            break

        main_dir = os.getcwd()
        today_date=(datetime.datetime.today()-datetime.timedelta(0)).strftime('%Y-%m-%d')
        file_path = f'{main_dir}\\Raj Chudasama\\{today_date}\\{property_name}'
        print(file_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            global subject
            fileName = part.get_filename()
            if bool(fileName):
                filePath = os.path.join(file_path, fileName)
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    fp1 = f'{main_dir}\\Raj Chudasama\\{today_date}\\'
    if os.path.exists(fp1):
        main_script()


def main_script():
    for i in range(0, 1):

        today_date = (datetime.datetime.today() - datetime.timedelta(0)).strftime('%Y-%m-%d')

        cwd = os.getcwd()

        path1 = cwd + '\\Raj Chudasama\\' + today_date

        arr = os.listdir(path1)

        for dir1 in arr:

            path2 = path1 + '\\' + dir1

            for file_path in glob.glob(path2 + '\\*.pdf'):

                file_name = os.path.basename(file_path)

                if file_name.startswith('EXPECTED ARRIVALS'):
                    expected_arrivals(file_path, path2)
                    print('Expected Arrivals generated...', today_date)

                if file_name.startswith('IN HOUSE'):
                    inhouseguests(file_path, path2)
                    print('In House guest list generated...', today_date)

                if file_name.startswith(('guest', 'gstlist')):
                    guest_list(file_path)
                    print('Guest List generated...', today_date)

                if file_name.startswith('arrivalllandscape'):
                    arrival_landscape_new(file_path)
                    print('Arrivals Landscape generated...', today_date)

                if file_name.startswith('remaining'):
                    remaining_arrivals(file_path)
                    print('Remining Arrivals generated...', today_date)

                for zippath in glob.iglob(os.path.join(path2, '*.txt')):
                    os.remove(zippath)




if __name__ == '__main__':
    email_automation()
