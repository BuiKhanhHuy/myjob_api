import math
from configs import table_export
from django.conf import settings
from helpers import helper
from django.core.mail import EmailMultiAlternatives


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # earth radius in kilometers

    # convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # calculate differences between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # apply Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return distance


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


def convert_data_with_en_key_to_vn_kew(data, key_dict, show_status_number=True):
    listNew = []
    try:
        i = 0
        while i < len(data) and i <= table_export.MAX_ROWS:
            dictNew = {}
            if show_status_number:
                dictNew[key_dict["stt"]] = i + 1
            for key, value in data[i].items():
                dictNew[key_dict[key]] = value
            listNew.append(dictNew)
            i += 1

    except Exception as ex:
        helper.print_log_error("convert_data_with_en_key_to_vn_kew", ex)
    return listNew


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
