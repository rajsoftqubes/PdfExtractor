
import datetime
import glob
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from utils import get_loggger

days=0

today_date = (datetime.datetime.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')
date1=(datetime.datetime.today() - datetime.timedelta(days)).strftime("%d-%b-%Y")

sender_address = 'raj.patel@softqubes.com'
sender_pass = 'pvbyhrtypexuurro'

receiver_address = ['raj@kriyahotels.com']
ccs = ['hardik.kanak@softqubes.com']
logger = get_loggger(f'Log_{today_date}')


def send_log_ind():
	try:
		mail_content = f"Log for today's pdf extraction"

		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = ','.join(receiver_address)
		message['Cc'] = ','.join(ccs)
		message['Subject'] = f'Log file for Date : {today_date}'
		message.attach(MIMEText(mail_content, 'plain'))

		logfile_name = f'G:\\Raj\\PdfExtractor\\logs\\Log_{today_date}.txt'
		filename = logfile_name.split('\\')[-1]
		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(logfile_name, "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
		message.attach(part)
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.starttls()
		session.login(sender_address, sender_pass)
		text = message.as_string()
		session.sendmail(sender_address, (receiver_address + ccs), text)
		session.quit()
		logger.info(f'Log mail sent.')

	except Exception as e:
		logger.debug(e)


if __name__ == '__main__':
	send_log_ind()
