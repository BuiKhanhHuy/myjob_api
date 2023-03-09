from configs import variable_system as var_sys
from helpers import utils, helper
from configs import variable_response as var_res
from rest_framework.decorators import api_view
from rest_framework import status
from .models import (
    Career
)


@api_view(http_method_names=["POST"])
def create_database(request):
    careers = ['Chứng khoán - Vàng', 'Tài chính - Tiền tệ', 'Bảo hiểm/ Tư vấn bảo hiểm', 'Đầu tư', 'Bất động sản',
               'Kế toán - Kiểm toán', 'Ngân hàng/ Tài Chính', 'Xây dựng', 'Kiến trúc - Thiết kế nội thất',
               'Khách sạn - Du lịch', 'Du lịch', 'Khách sạn - Nhà hàng', 'Sản xuất', 'Công nghệ cao', 'Công nghiệp',
               'Dệt may - Da giày', 'In ấn - Xuất bản', 'Lao động phổ thông', 'Nông - Lâm - Ngư nghiệp',
               'Ô tô - Xe máy', 'Thủ công mỹ nghệ', 'Vật tư/Thiết bị/Mua hàng', 'Làm thêm', 'Làm bán thời gian',
               'Nhân viên trông quán internet', 'Promotion Girl/ Boy (PG-PB)', 'Sinh viên làm thêm', 'Thực tập',
               'Kinh doanh - Thương mại', 'Bán hàng', 'Nhân viên kinh doanh', 'Quản trị kinh doanh', 'Xuất - Nhập khẩu',
               'Công nghệ thông tin', 'Games', 'IT phần cứng/mạng', 'IT phần mềm', 'Thiết kế đồ họa - Web',
               'Thương mại điện tử', 'Truyền thông - PR', 'Biên tập/ Báo chí/ Truyền hình', 'Marketing - PR',
               'Tiếp thị - Quảng cáo', 'Tổ chức sự kiện - Quà tặng', 'Viễn thông', 'Bưu chính', 'Điện tử viễn thông',
               'Hàng tiêu dùng', 'Hàng gia dụng', 'Mỹ phẩm - Trang sức', 'Thời trang', 'Thực phẩm - Đồ uống',
               'Dịch vụ - Hỗ trợ', 'Bảo vệ/ An ninh/ Vệ sỹ', 'Phiên dịch/ Ngoại ngữ', 'Dịch vụ', 'Giáo dục - Đào tạo',
               'Hàng hải', 'Hàng không', 'Người giúp việc/ Phục vụ/ Tạp vụ', 'Pháp luật/ Pháp lý',
               'Tư vấn/ Chăm sóc khách hàng', 'Vận tải - Lái xe/ Tài xế', 'Y tế - Dược', 'Kỹ thuật - Công nghệ',
               'Cơ khí - Chế tạo', 'Dầu khí - Hóa chất', 'Điện - Điện tử - Điện lạnh', 'Hóa học - Sinh học', 'Kỹ thuật',
               'Kỹ thuật ứng dụng', 'Hành chính - Nhân sự', 'Hành chính - Văn phòng', 'Nhân sự', 'Thư ký - Trợ lý',
               'Ngành nghề khác', 'Hoạch định - Dự án', 'Nghệ thuật/ Điện ảnh', 'Thiết kế - Mỹ thuật',
               'Quan hệ đối ngoại', 'Xuất khẩu lao động', 'Startup', 'Freelance', 'Tính chất công việc',
               'QA-QC/ Thẩm định/ Giám định', 'Môi trường', 'Phi chính phủ/ Phi lợi nhuận', 'Lương cao',
               'Việc làm cấp cao', 'Việc myjob_common_careerlàm Tết', 'Công chức / Viên chức', 'Phát triển thị trường',
               'Giao nhận/ Vận chuyển/ Kho bãi', 'Làm đẹp/ Thể lực/ Spa', 'Thể dục/ Thể thao', 'Vận tải',
               'Nghệ thuật/ Giải trí']
    if not Career.objects.exists():
        for career in careers:
            Career.objects.create(name=career)

    return var_res.response_data()


@api_view(http_method_names=["GET"])
def get_all_config(request):
    try:
        gender_options = utils.convert_tuple_choices_to_option_list(var_sys.GENDER_CHOICES)
        marital_status_options = utils.convert_tuple_choices_to_option_list(var_sys.MARITAL_STATUS_CHOICES)
        language_options = utils.convert_tuple_choices_to_option_list(var_sys.LANGUAGE_CHOICES)
        language_level_options = utils.convert_tuple_choices_to_option_list(var_sys.LANGUAGE_LEVEL_CHOICES)
        position_options = utils.convert_tuple_choices_to_option_list(var_sys.POSITION_CHOICES)
        type_of_workplace_options = utils.convert_tuple_choices_to_option_list(var_sys.TYPE_OF_WORKPLACE_CHOICES)
        job_type_options = utils.convert_tuple_choices_to_option_list(var_sys.JOB_TYPE_CHOICES)
        experience_options = utils.convert_tuple_choices_to_option_list(var_sys.EXPERIENCE_CHOICES)
        employee_size_options = utils.convert_tuple_choices_to_option_list(var_sys.EMPLOYEE_SIZE_CHOICES)
        application_status_options = utils.convert_tuple_choices_to_option_list(var_sys.APPLICATION_STATUS)

        res_data = {
            "genderOptions": gender_options,
            "maritalStatusOptions": marital_status_options,
            "languageOptions": language_options,
            "languageLevelOptions": language_level_options,
            "positionOptions": position_options,
            "typeOfWorkplaceOptions": type_of_workplace_options,
            "jobTypeOptions": job_type_options,
            "experienceOptions": experience_options,
            "employeeSizeOptions": employee_size_options,
            "applicationStatusOptions": application_status_options
        }
    except Exception as ex:
        helper.print_log_error(func_name="get_all_config", error=ex)
        return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     data=None, message="Lỗi hệ thống!")
    else:
        return var_res.response_data(data=res_data)
