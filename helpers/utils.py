from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def convert_tuple_or_list_to_options(values):
    result_list = []
    result_dict = {}
    for row in values:
        option_dict = {
            "id": row[0],
            "name": row[1],
        }
        result_list.append(option_dict)
        result_dict[row[0]] = row[1]
    return result_list, result_dict


def send_mail(subject, text_content, email_html, to=None, cc=None, bcc=None):
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
        cc=cc,
        bcc=bcc
    )
    email.attach_alternative(email_html, 'text/html')
    return email.send()
