from django.conf import settings
from django.contrib.sites.models import Site
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
import logging
import socket


def mail_config_tester():
    the_key = getattr(settings, "EMAIL_KEY", None)
    print(f'Mail key {the_key}')
    return the_key


def send_email_old(body, destination, subject):

    try:
        sg = SendGridAPIClient(getattr(settings, "EMAIL_KEY", None))
        sender = getattr(settings, "EMAIL_FROM", None)
        message = Mail(
            from_email=sender,
            to_emails=destination,
            subject=subject,
            html_content=body)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
        return 0, ''
    except Exception as e:
        logging.getLogger("info_logger").info(f"Error: {e}")
        return 1, sender


def send_email(**email_kwargs):
    """
    Sending an email
    :param email_kwargs: all the keyword arguments passed in
    :return: int 0/1 to show pass or fail
            str: null if no issue
                not null with the sender email
    """
    try:
        sender = getattr(settings, "EMAIL_FROM", None)
        to_emails = [
            To(email='thierrydna@me.com',
               name='BD Manager',  #this will be the content shown in the 'to' field
               subject='Web Enquiry'),  # overrides the subject sent
            To(email=email_kwargs.get('email'),
               name=email_kwargs.get('full_name'),
               subject='Your enquiry to A Sharp Systems'),
        ]
        sg = SendGridAPIClient(getattr(settings, "EMAIL_KEY", None))

        message = Mail(
            from_email=sender,
            # to_emails=[(email_kwargs.get('email')), (sender)],
            to_emails=to_emails,
            subject=email_kwargs.get('subject'),
            html_content=email_kwargs.get('content'),
            is_multiple=True)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
        return 0, ''
    except Exception as e:
        logging.getLogger("info_logger").info(f"Error: {e}")
        return 1, sender


def email_main(existing_user, **email_kwargs):
    '''  Main code to build the components from key, invitee, user_name, group_name, destination, subject     '''
    body = email_kwargs.get('body')
    send_success, sender  = send_email(body, email_kwargs.get('destination'), email_kwargs.get('subject'))
    # result will be 0 if success or the body if failed
    return send_success, sender

