import json
from configs import variable_system as var_sys
from django.conf import settings
from helpers import utils, helper
from configs import variable_response as var_res, paginations
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework import status
from .models import (
    Career,
    City,
    District,
)
from .serializers import (
    CareerSerializer
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
        # system
        completed_profile_tuple = utils.convert_tuple_or_list_to_options(var_sys.COMPLETED_PROFILE)
        gender_tuple = utils.convert_tuple_or_list_to_options(var_sys.GENDER_CHOICES)
        marital_status_tuple = utils.convert_tuple_or_list_to_options(var_sys.MARITAL_STATUS_CHOICES)
        language_tuple = utils.convert_tuple_or_list_to_options(var_sys.LANGUAGE_CHOICES)
        language_level_tuple = utils.convert_tuple_or_list_to_options(var_sys.LANGUAGE_LEVEL_CHOICES)
        position_tuple = utils.convert_tuple_or_list_to_options(var_sys.POSITION_CHOICES)
        type_of_workplace_tuple = utils.convert_tuple_or_list_to_options(var_sys.TYPE_OF_WORKPLACE_CHOICES)
        job_type_tuple = utils.convert_tuple_or_list_to_options(var_sys.JOB_TYPE_CHOICES)
        academic_level_tuple = utils.convert_tuple_or_list_to_options(var_sys.ACADEMIC_LEVEL)
        experience_tuple = utils.convert_tuple_or_list_to_options(var_sys.EXPERIENCE_CHOICES)
        employee_size_tuple = utils.convert_tuple_or_list_to_options(var_sys.EMPLOYEE_SIZE_CHOICES)
        application_status_tuple = utils.convert_tuple_or_list_to_options(var_sys.APPLICATION_STATUS)
        frequency_notification_tuple = utils.convert_tuple_or_list_to_options(var_sys.FREQUENCY_NOTIFICATION)

        # database
        cities = City.objects.values_list("id", "name")
        careers = Career.objects.values_list("id", "name")
        city_tuple = utils.convert_tuple_or_list_to_options(cities)
        career_tuple = utils.convert_tuple_or_list_to_options(careers)

        completed_profile_options = completed_profile_tuple[0]
        gender_options = gender_tuple[0]
        marital_status_options = marital_status_tuple[0]
        language_options = language_tuple[0]
        language_level_options = language_level_tuple[0]
        position_options = position_tuple[0]
        type_of_workplace_options = type_of_workplace_tuple[0]
        job_type_options = job_type_tuple[0]
        experience_options = experience_tuple[0]
        academic_level_options = academic_level_tuple[0]
        employee_size_options = employee_size_tuple[0]
        application_status_options = application_status_tuple[0]
        city_options = city_tuple[0]
        career_options = career_tuple[0]
        frequency_notification_options = frequency_notification_tuple[0]

        completed_profile_dict = completed_profile_tuple[1]
        gender_dict = gender_tuple[1]
        marital_status_dict = marital_status_tuple[1]
        language_dict = language_tuple[1]
        language_level_dict = language_level_tuple[1]
        position_dict = position_tuple[1]
        type_of_workplace_dict = type_of_workplace_tuple[1]
        job_type_dict = job_type_tuple[1]
        experience_dict = experience_tuple[1]
        academic_level_dict = academic_level_tuple[1]
        employee_size_dict = employee_size_tuple[1]
        application_status_dict = application_status_tuple[1]
        city_dict = city_tuple[1]
        career_dict = career_tuple[1]
        frequency_notification_dict = frequency_notification_tuple[1]

        res_data = {
            "completedProfileOptions": completed_profile_options,
            "genderOptions": gender_options,
            "maritalStatusOptions": marital_status_options,
            "languageOptions": language_options,
            "languageLevelOptions": language_level_options,
            "positionOptions": position_options,
            "typeOfWorkplaceOptions": type_of_workplace_options,
            "jobTypeOptions": job_type_options,
            "experienceOptions": experience_options,
            "academicLevelOptions": academic_level_options,
            "employeeSizeOptions": employee_size_options,
            "applicationStatusOptions": application_status_options,
            "cityOptions": city_options,
            "careerOptions": career_options,
            "frequencyNotificationOptions": frequency_notification_options,

            "completedProfileDict": completed_profile_dict,
            "genderDict": gender_dict,
            "maritalStatusDict": marital_status_dict,
            "languageDict": language_dict,
            "languageLevelDict": language_level_dict,
            "positionDict": position_dict,
            "typeOfWorkplaceDict": type_of_workplace_dict,
            "jobTypeDict": job_type_dict,
            "experienceDict": experience_dict,
            "academicLevelDict": academic_level_dict,
            "employeeSizeDict": employee_size_dict,
            "applicationStatusDict": application_status_dict,
            "cityDict": city_dict,
            "careerDict": career_dict,
            "frequencyNotificationDict": frequency_notification_dict,
        }
    except Exception as ex:
        helper.print_log_error(func_name="get_all_config", error=ex)
        return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     data=None)
    else:
        return var_res.response_data(data=res_data)


@api_view(http_method_names=["GET"])
def get_districts(request):
    params = request.query_params
    city_id = params.get('cityId', None)

    try:
        district_queryset = District.objects
        if city_id:
            district_queryset = district_queryset.filter(city_id=city_id)

        districts = district_queryset.values_list("id", "name")
        district_options = utils.convert_tuple_or_list_to_options(districts)[0]
    except Exception as ex:
        helper.print_log_error(func_name="get_districts", error=ex)
        return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     data=None)
    else:
        return var_res.response_data(data=district_options)


@api_view(http_method_names=["GET"])
def get_top_10_careers(request):
    try:
        queryset = Career.objects.annotate(num_job_posts=Count('job_posts')).order_by('-num_job_posts')[:10]
        serializer = CareerSerializer(queryset, many=True, fields=['id', 'name', 'iconUrl', 'jobPostTotal'])
    except Exception as ex:
        helper.print_log_error("get_top_careers", ex)
        return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return var_res.response_data(data=serializer.data)


@api_view(http_method_names=["GET"])
def get_all_careers(request):
    try:
        paginator = paginations.CustomPagination()

        queryset = Career.objects
        kw = request.query_params.get("kw", None)
        if kw:
            queryset = queryset.filter(name__icontains=kw)
        queryset = queryset.all().order_by('id')

        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CareerSerializer(page, many=True, fields=['id', 'name', 'iconUrl', 'jobPostTotal'])
            return paginator.get_paginated_response(serializer.data)

        serializer = CareerSerializer(queryset, many=True, fields=['id', 'name', 'iconUrl', 'jobPostTotal'])
        return var_res.response_data(data=serializer.data)
    except Exception as ex:
        helper.print_log_error("get_all_careers", ex)
        return var_res.response_data(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
