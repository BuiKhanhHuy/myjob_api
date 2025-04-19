from django.conf import settings

ADMIN = 'ADMIN'
EMPLOYER = 'EMPLOYER'
JOB_SEEKER = 'JOB_SEEKER'

CV_WEBSITE = "WEBSITE"
CV_UPLOAD = "UPLOAD"

NOTIFICATION_TYPE = {
    "SYSTEM": "SYSTEM",
    "EMPLOYER_VIEWED_RESUME": "EMPLOYER_VIEWED_RESUME",
    "EMPLOYER_SAVED_RESUME": "EMPLOYER_SAVED_RESUME",
    "APPLY_STATUS": "APPLY_STATUS",
    "COMPANY_FOLLOWED": "COMPANY_FOLLOWED",
    "APPLY_JOB": "APPLY_JOB",
    "POST_VERIFY_REQUIRED": "POST_VERIFY_REQUIRED",
    "POST_VERIFY_RESULT": "POST_VERIFY_RESULT"
}
NO_IMAGE = f"{settings.CLOUDINARY_PATH.format('1')}{settings.CLOUDINARY_DIRECTORY['system']}no_image.png"
NOTIFICATION_IMAGE_DEFAULT = f"{settings.CLOUDINARY_PATH.format('1')}{settings.CLOUDINARY_DIRECTORY['system']}notification_image_default.png"

DATE_TIME_FORMAT = {
    "dmY": "%d/%m/%Y",
    "Ymd": "%Y-%m-%d",
    "ISO8601": "%Y-%m-%dT%H:%M:%S.%fZ"
}

AUTH_PROVIDERS = (('email', 'email'), ('facebook',
                  'facebook'), ('google', 'google'))

AVATAR_DEFAULT = {
    "AVATAR": f"{settings.CLOUDINARY_PATH.format('1')}{settings.CLOUDINARY_DIRECTORY['system']}avt_default.jpg",
    "COMPANY_LOGO": f"{settings.CLOUDINARY_PATH.format('1')}{settings.CLOUDINARY_DIRECTORY['system']}company_logo_default.png",
    "COMPANY_COVER_IMAGE": f"{settings.CLOUDINARY_PATH.format('1')}{settings.CLOUDINARY_DIRECTORY['system']}company_cover_image_default.jpg",
}

COMPANY_INFO = {
    "DARK_LOGO_LINK": f"{settings.CLOUDINARY_PATH.format('1')}{settings.CLOUDINARY_DIRECTORY['system']}job_dark_logo.png",
    "LIGHT_LOGO_LINK": f"{settings.CLOUDINARY_PATH.format('1')}{settings.CLOUDINARY_DIRECTORY['system']}myjob_light_logo.png",
    "EMAIL": "myjob.support@gmail.com",
    "PHONE": "0888-425-094",
    "ADDRESS": "1242 QL1A, Tân Tạo A, Bình Tân, TP. Hồ Chí Minh",
    "WORK_TIME": "8:00 - 17:30 (Thứ 2 - Thứ 6)",
    "MY_COMPANY_NAME": settings.COMPANY_NAME
}

ABOUT_US_IMAGE_URLS = {
    "JOB_SEEKER": {
        # TODO: Upload Cloudinary later
        "FEEDBACK_GUIDE": "https://i.postimg.cc/5t7fJjLG/Screenshot-2025-04-12-at-14-43-12.png",
        "ACHIEVEMENTS": "https://i.postimg.cc/WpnKdxhm/dd346eca-7a6a-44a0-8816-f9bee25ac68e.png",
    },
    "EMPLOYER": {
        # TODO: Upload Cloudinary later
        "FEEDBACK_GUIDE": "https://i.postimg.cc/sgCLBy32/Screenshot-2025-04-12-at-15-28-12.png",
        "ACHIEVEMENTS": "https://i.postimg.cc/WpnKdxhm/dd346eca-7a6a-44a0-8816-f9bee25ac68e.png",
    }
}

# TODO: Upload Cloudinary later
CHATBOT_ICONS = {
    # Job Seeker
    "job_seeker_search_job": "https://img.icons8.com/?size=100&id=132&format=png",
    "job_seeker_search_company": "https://img.icons8.com/?size=100&id=102675&format=png",
    "job_seeker_manage_profile": "https://img.icons8.com/?size=100&id=20317&format=png",
    "job_seeker_track_application_status": "https://img.icons8.com/?size=100&id=62774&format=png",
    "job_seeker_manage_all_profile": "https://img.icons8.com/?size=100&id=11733&format=png",
    "job_seeker_myjob_profile": "https://img.icons8.com/?size=100&id=63384&format=png",
    "job_seeker_attached_profile": "https://img.icons8.com/?size=100&id=123834&format=png",
    "job_seeker_about_us_target_1": "https://img.icons8.com/?size=100&id=20884&format=png",
    "job_seeker_about_us_target_2": "https://img.icons8.com/?size=100&id=58125&format=png",
    "job_seeker_about_us_target_3": "https://img.icons8.com/?size=100&id=345&format=png",
    "job_seeker_about_us_target_4": "https://img.icons8.com/?size=100&id=54481&format=png",
    # Employer
    "employer_search_candidate": "https://img.icons8.com/?size=100&id=132&format=png",
    "employer_manage_candidate": "https://img.icons8.com/?size=100&id=20317&format=png",
    "employer_update_company_info": "https://img.icons8.com/?size=100&id=102675&format=png",
    # Common
    "common_feedback": "https://img.icons8.com/?size=100&id=52209&format=png",
    "common_support": "https://img.icons8.com/?size=100&id=97144&format=png",
    "common_about_us": "https://img.icons8.com/?size=100&id=3439&format=png",
    "common_notification": "https://img.icons8.com/?size=100&id=11642&format=png",
    "common_login": "https://img.icons8.com/?size=100&id=djM90N1WNk5W&format=png",
    "common_account_and_password": "https://img.icons8.com/?size=100&id=7820&format=png",
    "common_faq": "https://img.icons8.com/?size=100&id=646&format=png",
    "common_how_to_use": "https://img.icons8.com/?size=100&id=iiBewifv8LwR&format=png",
    "common_chat_with_us": "https://img.icons8.com/?size=100&id=1361&format=png",
    "common_social": "https://img.icons8.com/?size=80&id=JqWLVxr0WCrz&format=png",
    "common_social_facebook": "https://img.icons8.com/?size=96&id=13912&format=png",
    "common_social_linkedin": "https://img.icons8.com/?size=100&id=8808&format=png",
    "common_social_youtube": "https://img.icons8.com/?size=96&id=108794&format=png",
    "common_social_instagram": "https://img.icons8.com/?size=160&id=BrU2BBoRXiWq&format=png",
    "common_privacy_policy": "https://img.icons8.com/?size=100&id=LeS5bIxWv2Kc&format=png",
}

SOCIAL_MEDIA_LINKS = {
    "facebook": "https://www.facebook.com/bkhuy/",
    "linkedin": "https://www.linkedin.com/in/huy-khanh-10041b20b/",
    "youtube": "https://www.youtube.com/channel/UCn49BvcP1w1mamaOSGTKVZw",
    "instagram": "https://www.instagram.com/huy.buikhanh_/",
    "github": "https://github.com/BuiKhanhHuy",
    "tiktok": "https://www.tiktok.com/@khanhhuy_27?_t=ZS-8vSsKoClLBB&_r=1",
    "twitter": "",
    "telegram": "",
}

PLATFORM_CHOICES = (
    ('WEB', 'Website'),
    ('APP', 'Ứng dụng')
)

LINK_GOOGLE_PLAY = "https://play.google.com/store/apps?hl=en"
LINK_APPSTORE = "https://www.apple.com/vn/app-store/"

ROLE_CHOICES = (
    (ADMIN, 'Quản trị viên'),
    (EMPLOYER, 'Nhà tuyển dụng'),
    (JOB_SEEKER, 'Người tìm việc')
)

JOB_POST_STATUS = (
    (1, 'Chờ duyệt'),
    (2, 'Không duyệt'),
    (3, 'Đã duyệt')
)

GENDER_CHOICES = (
    ('M', 'Nam'),
    ('F', 'Nữ'),
    ('O', 'Khác')
)

MARITAL_STATUS_CHOICES = (
    ('S', 'Độc thân'),
    ('M', 'Đã kết hôn')
)

LANGUAGE_CHOICES = (
    (1, 'Việt Nam'),
    (2, 'Anh'),
    (3, 'Nhật Bản'),
    (4, 'Pháp'),
    (5, 'Trung Quốc'),
    (6, 'Nga'),
    (7, 'Hàn Quốc'),
    (8, 'Đức'),
    (9, 'Ý'),
    (10, 'Ả Rập'),
    (11, 'Khác'),
)

LANGUAGE_LEVEL_CHOICES = (
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),
    (5, 'Level 5')
)

POSITION_CHOICES = (
    (1, 'Quản lý cấp cao'),
    (2, 'Quản lý cấp trung'),
    (3, 'Quản lý nhóm- giám sát'),
    (4, 'Chuyên gia'),
    (5, 'Chuyên viên- nhân viên'),
    (6, 'Cộng tác viên'),
)

TYPE_OF_WORKPLACE_CHOICES = (
    (1, 'Làm việc tại văn phòng'),
    (2, 'Làm việc kết hợp'),
    (3, 'Làm việc tại nhà')
)

# OK
JOB_TYPE_CHOICES = (
    (1, 'Toàn thời gian cố định'),
    (2, 'Toàn thời gian tạm thời'),
    (3, 'Bán thời gian cố định'),
    (4, 'Bán thời gian tạm thời'),
    (5, 'Theo hợp đồng tư vấn'),
    (6, 'Thực tập'),
    (7, 'Khác'),
)

EXPERIENCE_CHOICES = (
    (1, 'Chưa có kinh nghiệm'),
    (2, 'Dưới 1 năm kinh nghiệm '),
    (3, '1 năm kinh nghiệm'),
    (4, '2 năm kinh nghiệm'),
    (5, '3 năm kinh nghiệm'),
    (6, '4 năm kinh nghiệm'),
    (7, '5 năm kinh nghiệm'),
    (8, 'Trên 5 năm kinh nghiệm')
)

ACADEMIC_LEVEL = (
    (1, 'Trên Đại học'),
    (2, 'Đại học'),
    (3, 'Cao đẳng'),
    (4, 'Trung cấp'),
    (5, 'Trung học'),
    (6, 'Chứng chỉ')
)

EMPLOYEE_SIZE_CHOICES = (
    (1, 'Dưới 10 nhân viên'),
    (2, '10 - 150 nhân viên'),
    (3, '150 - 300 nhân viên'),
    (4, 'Trên 300 nhân viên'),
)

APPLICATION_STATUS = (
    (1, 'Chờ xác nhận'),
    (2, 'Đã liên hệ'),
    (3, 'Đã test'),
    (4, 'Đã phỏng vấn'),
    (5, 'Trúng tuyển'),
    (6, 'Không trúng tuyển')
)

FREQUENCY_NOTIFICATION = (
    (1, 'Mỗi ngày'),
    (2, '3 Ngày / lần'),
    (3, '1 Tuần / 1 lần'),
)

DESCRIPTION_LOCATION = (
    (1, 'TOP_LEFT'),
    (2, 'TOP_RIGHT'),
    (3, 'BOTTOM_LEFT'),
    (4, 'BOTTOM_RIGHT')
)

BANNER_TYPE = (
    (1, 'HOME'),
    (2, 'MAIN_JOB_RIGHT'),
)
