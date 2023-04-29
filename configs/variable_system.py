ADMIN = 'ADMIN'
EMPLOYER = 'EMPLOYER'
JOB_SEEKER = 'JOB_SEEKER'

CV_WEBSITE = "WEBSITE"
CV_UPLOAD = "UPLOAD"

NOTIFICATION_TYPE = {
    "SYSTEM": "SYSTEM",
    "WELCOME": "WELCOME",
    "EMPLOYER_VIEWED_RESUME": "EMPLOYER_VIEWED_RESUME",
    "EMPLOYER_SAVED_RESUME": "EMPLOYER_SAVED_RESUME",
    "APPLY_STATUS": "APPLY_STATUS",
    "COMPANY_FOLLOWED": "COMPANY_FOLLOWED",
    "POST_VERIFY_REQUIRED": "POST_VERIFY_REQUIRED"
}

DATE_TIME_FORMAT = {
    "dmY": "%d/%m/%Y",
    "Ymd": "%Y-%m-%d",
    "ISO8601": "%Y-%m-%dT%H:%M:%S.%fZ"
}

AUTH_PROVIDERS = (('email', 'email'), ('facebook', 'facebook'), ('google', 'google'))

AVATAR_DEFAULT = {
    "AVATAR": "https://res.cloudinary.com/dtnpj540t/image/upload/v1680687265/my-job/images_default/avt_default.jpg",
    "COMPANY_LOGO": "https://img.icons8.com/external-xnimrodx-lineal-gradient-xnimrodx/1x/external-company-town-xnimrodx-lineal-gradient-xnimrodx-4.png",
    "COMPANY_COVER_IMAGE": "https://img.freepik.com/free-vector/purple-abstract-background_1340-17009.jpg?w=1380&t=st=1680457096~exp=1680457696~hmac=dce6634b13f28ecbe48a8de53421b99783d4b3f9dd4286d6ea2e68176cbfc083",
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

LINK_GOOGLE_PLAY = ""
LINK_APPSTORE = ""

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
