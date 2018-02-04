from django.core.mail import send_mail
from django.conf import settings

def send_email(email_user=None, token=None):

    if email_user is None or token is None:
        return -1

    email_subject = "OTP"
    email_message = "Your otp is : " + token
    email_from = settings.EMAIL_FROM
    email_recipient_list = [email_user]
    email_status = send_mail(subject=email_subject, message=email_message, from_email=email_from, recipient_list=email_recipient_list)
    return email_status


