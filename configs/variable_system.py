AUTH_PROVIDERS = (('email', 'email'), ('facebook', 'facebook'), ('google', 'google'))

AVATAR_DEFAULT = {
    "USER_AVT": "https://cloudinary.com/console/c-7145a9883ab06f170cab39cb3463a5/media_library/folders" \
                "/c16d59372d09573f486adb6bf8d49e1cb3 ",
    "LOGO": "https://cloudinary.com/console/c-7145a9883ab06f170cab39cb3463a5/media_library/folders" \
            "/c16d59372d09573f486adb6bf8d49e1cb3 "
}

PLATFORM_CHOICES = (
    ('WEB', 'Website'),
    ('APP', 'Ứng dụng')
)

ROLE_CHOICES = (
    ('ADMIN', 'Quản trị viên'),
    ('EMPLOYER', 'Nhà tuyển dụng'),
    ('JOB_SEEKER', 'Người tìm việc')
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
    (1, ''),
)

LANGUAGE_LEVEL_CHOICES = (
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),
    (5, 'Level 5')
)

POSITION_CHOICES = (
    (1, ''),
)

TYPE_OF_WORKPLACE_CHOICES = (
    (1, 'Làm việc tại văn phòng'),
    (2, 'Làm việc kết hợp'),
    (3, 'Làm việc tại nhà')
)

JOB_TYPE_CHOICES = (
    (1, ''),
)

EXPERIENCE_CHOICES = (
    (1, ''),
)

EMPLOYEE_SIZE_CHOICES = (
    (1, ''),
)

APPLICATION_STATUS = (
    (1, 'Chưa cập nhật'),
    (2, 'Chờ duyệt'),
    (3, 'Đã duyệt'),
    (4, 'Từ chối')
)
