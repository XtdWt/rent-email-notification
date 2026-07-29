import datetime
import logging
import os
import smtplib
import ssl

import pytz
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def send_mail(subject: str, message: str, e_to: str, e_from: str, password: str) -> None:
    port = 465  # For SSL
    full_msg = f"Subject: {subject}\n\n{message}"
    logger.debug("Establishing connection!")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(user=e_from, password=password)
        logger.debug("Successfully logged in!")
        server.sendmail(from_addr=e_from, to_addrs=e_to, msg=full_msg)
        logger.debug("Mail sent!")
    logger.debug("Connection successfully closed!")


def check_date(start_date: datetime.date) -> tuple[bool, datetime.date]:
    today_date = datetime.datetime.now(pytz.timezone("Australia/Sydney")).date()
    day_delta = today_date - start_date
    if day_delta.days % 14 == 0:
        return True, today_date
    else:
        return False, today_date


def main():
    # check that the date is correct
    start_date_str = os.getenv("START_DATE")
    if start_date_str is None:
        raise ValueError("`START_DATE` not properly set up in env")
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    is_right_day, today = check_date(start_date)
    if not is_right_day:
        logger.info(f"Today: {today} is not the right week!")
        return None
    logger.info(f"Today: {today} is the right week!")
    subject = "[AUTO] Rent Due"
    msg = "Reminder to pay rent today!!!"
    email_to = os.getenv("EMAIL_TO")
    email_from = os.getenv("EMAIL_FROM")
    password = os.getenv("EMAIL_PASSWORD")
    if email_to is None or email_from is None or password is None:
        raise ValueError("One of `EMAIL_TO`, `EMAIL_FROM` or `EMAIL_PASSWORD` not properly set up in env")
    send_mail(subject, msg, email_to, email_from, password)
    logger.info(f"Mail sent on: {today} from {email_from} to {email_to}!")


if __name__ == "__main__":
    main()
