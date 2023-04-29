from celery import shared_task
from firebase_admin import db
from datetime import datetime


@shared_task
def add_notification_to_user(title, content, type_name, content_of_type=None, user_id_list=None):
    if user_id_list is None:
        user_id_list = []
    current_timestamp = datetime.timestamp(datetime.now())

    ref = db.reference()
    notification_ref = ref.child("notifications")
    for user_id in user_id_list:
        notification = {
            "title": title,
            "content": content,
            "time": current_timestamp,
            "type": type_name,
            type_name: content_of_type
        }
        notification_ref.child(str(user_id)).push(notification)
