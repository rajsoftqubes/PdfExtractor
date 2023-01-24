import datetime
import glob
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

days=0

today_date = (datetime.datetime.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')
date1=(datetime.datetime.today() - datetime.timedelta(days)).strftime("%d-%b-%Y")


def get_loggger(filename):
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_formatter = logging.Formatter('[%(asctime)s][%(name)s][Line %(lineno)d]'
                                         '[%(levelname)s]:%(message)s')

    file_handler = logging.FileHandler(f'logs/{filename}.log', mode='w')

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logger_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logger_formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = get_loggger(f'Log_{today_date}')


def mail_sent(file_path, property_name, sender_mail):
    try:
        logger.info(f'Sending mail for {property_name}')
        mail_content = f'Here is the excel reports for {property_name}'

        sender_address = 'raj.patel@softqubes.com'
        sender_pass = 'inunrirddnttkjms'
        receiver_address = 'raj@kriyahotels.com'

        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['CC'] = 'hardik.kanak@softqubes.com'
        message['Subject'] = f'Sales Reports for {property_name} : {today_date}'
        message.attach(MIMEText(mail_content, 'plain'))

        for file in glob.glob(file_path + '\\*.xlsx'):
            excelfile_name = file.split('\\')[-1]
            attach_file_name = file
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attach_file_name, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{excelfile_name}"')
            message.attach(part)

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()

        logger.info(f'Mail sent for {property_name}')
        logger.info('\n')
    except Exception as e:
        logger.debug(e)


def send_log():
    try:

        mail_content = f"Log for today's pdf extraction"

        sender_address = 'raj.patel@softqubes.com'
        sender_pass = 'inunrirddnttkjms'
        receiver_address = 'raj@kriyahotels.com'

        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = f'Log for : {today_date}'
        message['CC']='hardik.kanak@softqubes.com'
        message.attach(MIMEText(mail_content, 'plain'))

        logfile_name = f'G:\\Raj\\PdfExtractor\\logs\\Log_{today_date}.log'

        filename=logfile_name.split('\\')[-1]

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(logfile_name, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        message.attach(part)

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
    except Exception as e:
        logger.debug(e)