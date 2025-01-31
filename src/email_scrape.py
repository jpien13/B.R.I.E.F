import logging
import imaplib
import os
import pytz
import datetime
import email
from connect_email import connect_to_email_server, get_unread_emails_from_sender, mark_emails_as_read
from email import policy
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta


def fetch_and_extract_email_text(mail, email_id):
    """
    Fetches an email by its ID and extracts all text from it.

    :param mail:
        The mail object that can be used to interact with the email server.
    :param email_id:
        The ID of the email to fetch and extract text from.
    :return:
        A string containing all the text extracted from the email.
    """
    try:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            logging.error(f"Failed to fetch email with ID {email_id}: {status}")
            raise Exception(f"Failed to fetch email with ID {email_id}: {status}")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email, policy=policy.default)

        text = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    text += part.get_payload(decode=True).decode()
                elif content_type == "text/html":
                    html_content = part.get_payload(decode=True).decode()
                    soup = BeautifulSoup(html_content, "html.parser")
                    text += soup.get_text()
        else:
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                text = msg.get_payload(decode=True).decode()
            elif content_type == "text/html":
                html_content = msg.get_payload(decode=True).decode()
                soup = BeautifulSoup(html_content, "html.parser")
                text = soup.get_text()
        return text

    except Exception as e:
        logging.error(f"Failed to fetch or extract text from email: {e}")
        raise

def main():
    """
    main function tests the email handling functionality by:
    1. Connecting to the email server.
    2. Retrieving unread emails from a specific sender.
    3. Extracting text from the retrieved emails (excluding links).
    4. Marking the retrieved emails as read.
    5. Logging the results for verification.
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
            for email_id in unread_email_ids:
                logging.info(f"Step 3: Extracting text from email ID {email_id}...")
                email_text = fetch_and_extract_email_text(mail, email_id)
                logging.info(f"Extracted text from email ID {email_id}:\n{email_text}\n")

            logging.info("Step 4: Marking the retrieved emails as read...")
            mark_emails_as_read(mail, unread_email_ids)
            logging.info("Successfully marked the emails as read.")

    except Exception as e:
        logging.error(f"An error occurred during testing: {e}")
    finally:
        if 'mail' in locals():
            logging.info("Step 5: Logging out from the email server...")
            mail.logout()
            logging.info("Successfully logged out.")


if __name__ == "__main__":
    main()