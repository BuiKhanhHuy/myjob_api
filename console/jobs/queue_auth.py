"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from celery import shared_task
from firebase_admin import firestore
from helpers import helper
from configs import variable_system as var_sys


@shared_task
def update_avatar(user_id, avatar_url):
    if not avatar_url:
        avatar_url = var_sys.AVATAR_DEFAULT["AVATAR"]
    database = firestore.client()
    account_ref = database.collection("accounts").document(str(user_id))
    try:
        account_doc = account_ref.get()
        if account_doc.exists:
            account = account_doc.to_dict()
            update_data = {
                "avatarUrl": avatar_url
            }

            if account["company"]:
                update_data.update({"company.imageUrl": avatar_url})
            account_ref.update(update_data)
    except Exception as e:
        helper.print_log_error("update_avatar", e)


@shared_task
def update_info(user_id, name):
    database = firestore.client()
    account_ref = database.collection("accounts").document(str(user_id))

    try:
        account_doc = account_ref.get()
        if account_doc.exists:
            account = account_doc.to_dict()
            update_data = {
                "name": name
            }

            if account["company"]:
                update_data.update({
                    "company.companyName": name,
                })
            account_ref.update(update_data)
    except Exception as e:
        helper.print_log_error("update_info", e)


