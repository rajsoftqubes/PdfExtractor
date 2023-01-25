import email
import imaplib
import json
import re
import os
import glob
from expected_arrivals_new import expected_arrivals
from gstchkin_csv import gstchkin_csv
from guestlist_csv import guestlist_csv
from inhouse_guestlist import inhouseguests
from arrivallanscape_new import arrival_landscape_new
from guest_list import guest_list
from remainingarrivals_df import remaining_arrivals
from utils import mail_sent, logger, today_date, date1, send_log

today_date = today_date


def email_automation():
    logger.info('Script is starting....\n')
    try:
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

        mail.select("Guestlist")

        type, data = mail.search(None, "(ON {0})".format(date1))

        total_mail=len(data[0].split())

        for index, num in enumerate(data[0].split()):
            typ, data = mail.fetch(num, '(RFC822)')

            raw_email = data[0][1]

            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            sender_mail = re.findall(r'(\w+\-sales\@kriyahotels.com)', raw_email_string)

            for s in sender_mail:
                property_name = obj[s]
                break

            main_dir = os.getcwd()

            file_path = f'{main_dir}\\Raj Chudasama\\{today_date}\\{property_name}'
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
                    full_path = os.path.join(file_path, fileName)
                    if not os.path.isfile(full_path):
                        fp = open(full_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
            logger.info(f'PDF files downloaded for {property_name}.')
            main_functions(file_path, property_name, sender_mail[0])

            if index==total_mail-1:

                send_log()

    except Exception as e:
        logger.debug(e)


def main_functions(file_path, property_name, sender_mail):
    try:
        pdf_files = []
        excel_files = []
        logger.info(f'Scraping starts for {property_name}.')

        for file in glob.glob(file_path+'\\*'):
            if '.pdf' in file or '.csv' in file:

                file_name = file.split('\\')[-1]
                logger.info(f'Getting data for {property_name}/{file_name}.')
                if '.pdf' in file_name:
                    pdf_files.append(file_name.split('.pdf')[0])
                elif '.csv' in file_name:
                    pdf_files.append(file_name.split('.csv')[0])

                if file_name.startswith('EXPECTED ARRIVALS') and file_name.endswith(".pdf"):

                    expected_arrivals(file)
                    logger.info(f'Excel is generated for {property_name}/{file_name}.')

                if file_name.startswith('IN HOUSE') and file_name.endswith(".pdf"):
                    inhouseguests(file)
                    logger.info(f'Excel is generated for {property_name}/{file_name}.')

                if file_name.startswith(('guest', 'gstlist')) and file_name.endswith(".pdf"):
                    guest_list(file)
                    logger.info(f'Excel is generated for {property_name}/{file_name}.')

                if file_name.startswith('arrivalllandscape') and file_name.endswith(".pdf"):
                    arrival_landscape_new(file)

                    logger.info(f'Excel is generated for {property_name}/{file_name}.')

                if file_name.startswith('remaining') and file_name.endswith(".pdf"):
                    remaining_arrivals(file)
                    logger.info(f'Excel is generated for {property_name}/{file_name}.')

                if file_name.startswith('gstchkin') and file_name.endswith(".csv"):
                    gstchkin_csv(file)
                    logger.info(f'Excel is generated for {property_name}/{file_name}.')

                if file_name.startswith('gstlista') and file_name.endswith(".csv"):
                    guestlist_csv(file)
                    logger.info(f'Excel is generated for {property_name}/{file_name}.')

                for zippath in glob.iglob(os.path.join(file_path, '*.txt')):
                    os.remove(zippath)

        for file in glob.glob(file_path + '\\*.xlsx'):
            excelfile_name = file.split('\\')[-1]
            excel_files.append(excelfile_name.split('.xlsx')[0])

        logger.info(f'All files are scraped for {property_name}')

        mail_sent(file_path, property_name, sender_mail)
    except Exception as e:
        logger.debug(e)


if __name__ == '__main__':
    email_automation()
