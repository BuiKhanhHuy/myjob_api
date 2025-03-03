# Error Messages
ERROR_MESSAGES = {
    'SOCIAL_EMAIL_EXISTS': 'Email tài khoản mạng xã hội bạn vừa liên kết đã tồn tại, vui lòng đăng nhập bằng tài khoản khác',
    'EMAIL_REQUIRED': 'Email is required for registration',
    'INVALID_PLATFORM': 'platform không hợp lệ.',
    'CONFIRM_PASSWORD_MISMATCH': 'Mật khẩu xác nhận không chính xác.',
    'CURRENT_PASSWORD_INCORRECT': 'Mật khẩu hiện tại không chính xác.',
    'CODE_REQUIRED': 'code là bắt buộc.',
    'TOKEN_REQUIRED': 'token là bắt buộc.',
    'EMAIL_EXISTS': 'Email đã tồn tại.',
    'COMPANY_NAME_EXISTS': 'Tên công ty đã tồn tại.',
    'COMPANY_EMAIL_EXISTS': 'Email công ty đã tồn tại.',
    'COMPANY_PHONE_EXISTS': 'Số điện thoại công ty đã tồn tại.',
    'COMPANY_TAX_CODE_EXISTS': 'Mã số thuế công ty đã tồn tại.',
    'INVALID_EMAIL': 'Email không chính xác.',
    'ACCOUNT_DISABLED': 'Tài khoản của bạn đã bị vô hiệu hóa. Vui lòng liên hệ với bộ phận chăm sóc khách hàng của chúng tôi. ',
    'INCORRECT_PASSWORD': 'Mật khẩu không chính xác.',
    'LOGIN_ERROR': 'Đã xảy ra lỗi trong quá trình đăng nhập.',
    'ACCOUNT_DEACTIVATED': 'Tài khoản đăng nhập với email này đã bị vô hiệu hóa hoặc đã không còn tồn tại. Vui lòng liên hệ với bộ phận chăm sóc khách hàng của chúng tôi để được hỗ trợ.',
    'INVALID_EMAIL_VERIFICATION': 'Rất tiếc, có vẻ như liên kết xác thực email không hợp lệ.',
    'EMAIL_VERIFICATION_EXPIRED': 'Rất tiếc, có vẻ như liên kết xác thực email đã hết hạn.',
    'PASSWORD_RESET_EMAIL_COOLDOWN': 'Bạn vừa gửi yêu cầu gửi email quên mật khẩu vui lòng kiểm tra hộp thư hoặc đợi thêm 2 phút để gửi lại email.',
    'EMAIL_NOT_REGISTERED': 'Email này chưa được sử dụng, bạn hãy đăng ký tham gia MyJob.',
    'INVALID_PASSWORD_RESET_LINK': 'Rất tiếc, có vẻ như liên kết xác nhận quên mật khẩu không hợp lệ',
    'PASSWORD_RESET_LINK_EXPIRED': 'Rất tiếc, có vẻ như liên kết xác nhận quên mật khẩu đã hết hạn',
    'INVALID_PASSWORD_RESET_CODE': 'Mã xác nhận quên mật khẩu không hợp lệ',
    'PASSWORD_RESET_CODE_EXPIRED': 'Mã xác nhận quên mật khẩu đã hết hạn',
    'CLOUDINARY_UPLOAD_ERROR': 'Something went wrong when upload image to cloudinary',
    'MAXIMUM_IMAGES':'Tối đa 15 ảnh',
    'MAXIMUM_CERTIFICATE': 'Tối đa 10 thông tin chứng chỉ',
    'MAXIMUM_EXPERIENCE': 'Tối đa 10 thông tin kinh nghiệm',
    'MAXIMUM_EDUCATION': 'Tối đa 10 thông tin học vấn',
    'MAXIMUM_LANGUAGE': 'Tối đa 10 thông tin ngôn ngữ',
    'MAXIMUM_ADVANCED': 'Tối đa 15 thông tin kỹ năng chuyên môn',
    'MAX_ACTIVE_JOB_NOTIFICATIONS': 'Tối đa 3 thông báo việc làm được bật',
    'PHONE_REQUIRED': 'Số điện thoại là bắt buộc',
    'INVALID_PHONE': 'Số điện thoại không hợp lệ',
    'USER_DOESNT_HAVE_JOB_SEEKER_PROFILE': "User doesn't have job_seeker_profile."
}

# Success Messages
SUCCESS_MESSAGES = {
    'EMAIL_VERIFIED': 'Email đã được xác thực.',
    'NOTIFICATION_DELETED': 'Thông báo đã được xóa.',
    'CHANGES_SAVED': 'Thay đổi đã được lưu.',
}

# System Messages
SYSTEM_MESSAGES = {
    'WELCOME_TITLE': 'Chào mừng bạn!',
    'WELCOME_JOBSEEKER': 'Chào mừng bạn đến với MyJob! Hãy sẵn sàng khám phá và trải nghiệm hệ thống của chúng tôi để tìm kiếm công việc mơ ước của bạn.',
    'WELCOME_EMPLOYER': 'Chào mừng bạn đến với MyJob! hệ thống giới thiệu việc làm nhanh chóng và tiện lợi để tìm kiếm nhân tài cho công ty của bạn!',
}

# Application Status Messages
APPLICATION_STATUS_MESSAGES = {
    'STATUS_UPDATED': 'Hồ sơ ứng tuyển của bạn vào vị trí "{job_name}" được cập nhật trạng thái sang "{status}"',
}

# Mail Messages
MAIL_MESSAGES = {
    'EMAIL_VERIFICATION_SUBJECT': 'Xác thực email',
    'PASSWORD_RESET_SUBJECT': 'Đặt lại mật khẩu',
    'ACCOUNT_DISABLED_SUBJECT': 'Thông báo: Tài khoản của bạn bị vô hiệu hóa',
    'JOB_NAME_SUBJECT': ['Việc làm {job_name}', 'và {total_result} công việc khác', 'cho bạn'],
    'PASSWORD_RESET_CODE': "{code} là mã xác nhận quên mật khẩu tài khoản MyJob của bạn",
    'JOB_NOTIFICATION_CANCEL_NO_SETTINGS': 'Send job notification email to {to_email} cancel. Due to not setting up job notifications',
    'JOB_NOTIFICATION_CANCEL_NO_JOBS': "Send job notification email to {to_email} cancel. Can't find any suitable job",
    'JOB_NOTIFICATION_FOUND': "Chúng tôi đã tìm thấy {total_result} công việc phù hợp với yêu cầu của bạn.",
}

# Notification Messages
NOTIFICATION_MESSAGES = {
    'NO_NOTIFICATIONS': 'Không có thông báo nào.',
    'DELETE_CONFIRMATION': 'Bạn có chắc chắn muốn xóa?',
    'CANNOT_UNDO': 'Hành động này không thể hoàn tác!',
    'APPLICANT_APPLICATION': 'Ứng viên {full_name} - {email}',
    'JOB_APPLICATION_SUBMITTED': 'Đã ứng tuyển vị trí "{job_name}"',
    'JOB_POSTING_REQUEST': 'Request to browse job posting "{job_post_title}"',
    'SYSTEM_NOTIFICATION': 'Thông báo hệ thống',
    'JOB_STATUS_CHANGE': 'Tin tuyển dụng "{job_name}" đã được chuyển sang trạng thái "{status}"',
    'DOWNLOAD_APP_MESSAGE': 'Tin nhắn được gửi từ {company_name}, Ứng dụng và Website giới thiệu việc làm. Với {company_name}, bạn có thể tìm kiếm các công việc phù hợp với nhu cầu và kinh nghiệm của mình chỉ trong vài phút. Để tải ứng dụng, bạn có thể truy cập vào link sau: Android: {link_google_play}; iOS: {link_appstore}. Hãy cùng trải nghiệm và tìm kiếm công việc mơ ước của bạn với {company_name} nhé!',
    'RESUME_SAVED': 'Đã lưu hồ sơ của bạn',
    'RESUME_UNSAVED': 'Đã huỷ lưu hồ sơ của bạn',
    'FOLLOW_NOTIFICATION': 'Đã follow bạn',
    'UNFOLLOW_NOTIFICATION': 'Đã unfollow bạn'
}
