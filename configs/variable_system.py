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
    "POST_VERIFY_REQUIRED": "POST_VERIFY_REQUIRED"
}
NOTIFICATION_IMAGE_DEFAULT = "https://res.cloudinary.com/dtnpj540t/image/upload/v1683799130/my-job/images_default/notification_image_default.png"

DATE_TIME_FORMAT = {
    "dmY": "%d/%m/%Y",
    "Ymd": "%Y-%m-%d",
    "ISO8601": "%Y-%m-%dT%H:%M:%S.%fZ"
}

AUTH_PROVIDERS = (('email', 'email'), ('facebook', 'facebook'), ('google', 'google'))

AVATAR_DEFAULT = {
    "AVATAR": "https://res.cloudinary.com/dtnpj540t/image/upload/v1680687265/my-job/images_default/avt_default.jpg",
    "COMPANY_LOGO": "https://res.cloudinary.com/dtnpj540t/image/upload/v1682831706/my-job/images_default/company_image_default.png",
    "COMPANY_COVER_IMAGE": "https://res.cloudinary.com/dtnpj540t/image/upload/v1683615297/my-job/images_default/company_cover_image_default.jpg",
}

COMPANY_INFO = {
    "DARK_LOGO_LINK": "https://res.cloudinary.com/dtnpj540t/image/upload/v1681050602/my-job/my-company-media/myjob-dark-logo.png",
    "LIGHT_LOGO_LINK": "https://res.cloudinary.com/dtnpj540t/image/upload/v1681050660/my-job/my-company-media/myjob-light-logo.png",
    "EMAIL": "myjob.contact00000@gmail.com",
    "PHONE": "0888-425-094",
    "ADDRESS": "1242 QL1A, Tân Tạo A, Bình Tân, TP. Hồ Chí Minh"
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

COMPLETED_PROFILE = (
    (1, ''),
    (2, ''),
    (3, ''),
    (4, ''),
    (5, ''),
    (6, ''),
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
    (3, 'Pháp'),
    (4, 'Đức'),
    (5, 'Nga'),
    (6, 'Trung Quốc'),
    (7, 'Hàn Quốc'),
    (8, 'Nhật Bản'),
    (9, 'Khác')
)

LANGUAGE_LEVEL_CHOICES = (
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),
    (5, 'Level 5')
)

POSITION_CHOICES = (
    (1, 'Sinh viên/Thực tập sinh'),
    (2, 'Mới tốt nghiệp'),
    (3, 'Nhân viên'),
    (4, 'Trưởng nhóm/Giám sát'),
    (5, 'Quản lý'),
    (6, 'Phó Giám đốc'),
    (7, 'Giám đốc'),
    (8, 'Tổng Giám đốc'),
    (9, 'Chủ tịch/Phó Chủ tịch')
)

TYPE_OF_WORKPLACE_CHOICES = (
    (1, 'Làm việc tại văn phòng'),
    (2, 'Làm việc kết hợp'),
    (3, 'Làm việc tại nhà')
)

JOB_TYPE_CHOICES = (
    (1, 'Nhân viên chính thức'),
    (2, 'Bán thời gian'),
    (3, 'Thời vụ - Nghề tự do'),
    (4, 'Thực tập')
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
    (6, 'Chứng chỉ nghề')
)

EMPLOYEE_SIZE_CHOICES = (
    (1, '1-9 nhân viên'),
    (2, '10-24 nhân viên'),
    (3, '25-99 nhân viên'),
    (4, '100-499 nhân viên'),
    (5, '500-1000 nhân viên'),
    (6, '1000+ nhân viên'),
    (7, '5000+ nhân viên'),
    (8, '10000+ nhân viên')
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