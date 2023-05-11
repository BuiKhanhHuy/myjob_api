from celery import shared_task
from firebase_admin import firestore
from google.cloud import firestore as google_cloud_firestore
from helpers import helper
from configs import variable_system as var_sys


@shared_task
def add_notification_to_user(title, content, type_name, image=None,
                             content_of_type=None, user_id_list=None):
    if not image:
        image = var_sys.NOTIFICATION_IMAGE_DEFAULT
    try:
        if user_id_list is None:
            user_id_list = []
        database = firestore.client()
        for user_id in user_id_list:
            notification = {
                "is_deleted": False,
                "is_read": False,
                "image": image,
                "title": title,
                "content": content,
                "time": google_cloud_firestore.SERVER_TIMESTAMP,
                "type": type_name,
                type_name: content_of_type
            }
            database.collection(u'users').document(str(user_id)).collection("notifications").add(notification)
    except Exception as ex:
        helper.print_log_error("add_notification_to_user", ex)
        return "Add notification failed!"
    else:
        return "Add notification successfully."

    # real time database
    # try:
    #     if user_id_list is None:
    #         user_id_list = []
    #     current_timestamp = datetime.timestamp(datetime.now())
    #
    #     ref = db.reference()
    #     notification_ref = ref.child("notifications")
    #     for user_id in user_id_list:
    #         notification = {
    #             "is_deleted": False,
    #             "image": image,
    #             "title": title,
    #             "content": content,
    #             "time": current_timestamp,
    #             "type": type_name,
    #             type_name: content_of_type
    #         }
    #         notification_ref.child(str(user_id)).push(notification)
    # except Exception as ex:
    #     helper.print_log_error("add_notification_to_user", ex)
    #     return "Add notification failed!"
    # else:
    #     return "Add notification successfully."
