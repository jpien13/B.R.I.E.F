import logging
import imaplib
import os
import pytz
import datetime
import email
from email import policy
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
# ====================================== INIT CONFIG ======================================
print("Initializing configuration...")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    logging.error("Email credentials not found in environment variables!")
    raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be set in environment variables")

print("Recieved EMAIL_ADDRESS and EMAIL_PASSWORD from environment variables.")
print(f"IMAP Server: {IMAP_SERVER}")
# ====================================== INIT CONFIG ======================================


def connect_to_email_server():
    """
    connect_to_email_server logs into the email server and selects the INBOX.
    It specifically logs in using the EMAIL_ADDRESS and EMAIL_PASSWORD from 
    the config file.

    :return:
        mail: The mail object that can be used to interact with the email server.
    """
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        logging.info(f'Connecting to {IMAP_SERVER}...')
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        logging.info(f"Successfully logged into {EMAIL_ADDRESS}")
        mail.select('INBOX')
        return mail
    except Exception as e:
        logging.error(f"Failed to connect to email server: {e}")
        raise

def get_unread_emails_from_sender(mail, sender_email):
    """
    get_unread_emails_from_sender retrieves all unread emails from a specific sender.
    
    :param mail:
        The mail object that can be used to interact with the email server.
    :param sender_email:
        The email address of the sender whose emails are to be retrieved.
    :return:
        A list of email IDs that match the criteria.
    """
    try:
       timezone = pytz.timezone('America/New_York')
       todays_date = datetime.now(timezone)
       search_date = todays_date.strftime('%d-%b-%Y')
       search_criteria = f'(FROM "{sender_email}" SINCE "{search_date}" UNSEEN)'

       logging.info(f"Local timezone: {timezone}")
       logging.info(f"Local time: {todays_date}")
       logging.info(f"Searching for emails from {sender_email} on {search_date}")
       logging.info(f"Using search criteria: {search_criteria}")

       status, email_ids = mail.search(None, search_criteria)
       
       if status != 'OK':
           logging.error(f"Failed to search for emails: {status}")
           raise Exception(f"Failed to search for emails: {status}")
       else:
            email_ids = email_ids[0].split()
            logging.info(f"Found {len(email_ids)} unread emails from {sender_email}")
            return email_ids
    except Exception as e:
        logging.error(f"Failed to get unread emails from {sender_email}: {e}")
        raise

def mark_emails_as_read(mail, email_ids):
    """
    mark_emails_as_read marks the specified email IDs as read by setting the SEEN flag.

    :param mail:
        The mail object that can be used to interact with the email server.
    :param email_ids:
        A list of email IDs to be marked as read.
    :return:
        None
    """
    try:
        for email_id in email_ids:
            status, response = mail.store(email_id, '+FLAGS', '\\SEEN')
            if status == 'OK':
                logging.info(f"Marked email ID {email_id} as read.")
            else:
                logging.error(f"Failed to mark email ID {email_id} as read: {response}")
    except Exception as e:
        logging.error(f"Failed to mark emails as read: {e}")
        raise

def main():
    """
    main function tests the email handling functionality by:
    1. Connecting to the email server.
    2. Retrieving unread emails from a specific sender.
    3. Marking the retrieved emails as read.
    4. Logging the results for verification.
    """
    try:
        logging.info("Step 1: Connecting to the email server...")
        mail = connect_to_email_server()
        logging.info("Successfully connected to the email server.")

        sender_email = input("Enter the sender's email address to retrieve unread emails: ")
        logging.info(f"Step 2: Retrieving unread emails from {sender_email}...")
        unread_email_ids = get_unread_emails_from_sender(mail, sender_email)

        if not unread_email_ids:
            logging.info(f"No unread emails found from {sender_email}")
        else:
            logging.info("Step 3: Marking the retrieved emails as read...")
            mark_emails_as_read(mail, unread_email_ids)
            logging.info("Successfully marked the emails as read.")

    except Exception as e:
        logging.error(f"An error occurred during testing: {e}")
    finally:
        if 'mail' in locals():
            logging.info("Step 4: Logging out from the email server...")
            mail.logout()
            logging.info("Successfully logged out.")

    

if __name__ == "__main__":
    main()