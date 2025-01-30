from connect_email import connect_to_email_server, get_unread_emails_from_sender, mark_emails_as_read
from email_scrape import fetch_and_extract_email_text
from summarizer import summarize_text
import logging

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
            logging.info("Making API call to summarize the email text...")
            summary = summarize_text(email_text, max_tokens=16384)
            print(summary)
            logging.info("Successfully summarized the email text.")

    except Exception as e:
        logging.error(f"An error occurred during testing: {e}")
    finally:
        if 'mail' in locals():
            logging.info("Step 5: Logging out from the email server...")
            mail.logout()
            logging.info("Successfully logged out.")


if __name__ == "__main__":
    main()