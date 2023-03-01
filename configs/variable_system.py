ADMIN = 'ADMIN'
EMPLOYER = 'EMPLOYER'
JOB_SEEKER = 'JOB_SEEKER'

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
    (ADMIN, 'Quản trị viên'),
    (EMPLOYER, 'Nhà tuyển dụng'),
    (JOB_SEEKER, 'Người tìm việc')
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
    (4, 'Thời vụ - Nghề tự do'),
    (5, 'Thực tập')
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
    (1, 'Chưa cập nhật'),
    (2, 'Chờ duyệt'),
    (3, 'Đã duyệt'),
    (4, 'Từ chối')
)
