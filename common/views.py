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
    data = {}
    nghe = [{'id': 1, 'name': 'Hành chính - Thư ký'}, {'id': 2, 'name': 'An ninh - Bảo vệ'},
            {'id': 3, 'name': 'Thiết kế - Sáng tạo nghệ thuật'}, {'id': 4, 'name': 'Kiến trúc - Thiết kế nội thất'},
            {'id': 5, 'name': 'Khách sạn - Nhà hàng - Du lịch'},
            {'id': 6, 'name': 'Bán buôn - Bán lẻ - Quản lý cửa hàng'},
            {'id': 7, 'name': 'IT Phần cứng - Mạng - Viễn Thông'}, {'id': 8, 'name': 'IT Phần mềm'},
            {'id': 9, 'name': 'Sản xuất - Lắp ráp - Chế biến'},
            {'id': 10, 'name': 'Vận hành máy - Bảo trì - Bảo dưỡng thiết bị'},
            {'id': 11, 'name': 'Nông - Lâm - Ngư nghiệp'}, {'id': 12, 'name': 'Marketing'},
            {'id': 13, 'name': 'Kinh doanh'}, {'id': 14, 'name': 'Thu mua - Kho Vận - Chuỗi cung ứng'},
            {'id': 15, 'name': 'Xuất Nhập Khẩu'}, {'id': 16, 'name': 'Vận Tải - Lái xe - Giao nhận'},
            {'id': 17, 'name': 'Kế toán'}, {'id': 18, 'name': 'Tài chính - Đầu tư'}, {'id': 19, 'name': 'Ngân hàng'},
            {'id': 20, 'name': 'Khai thác năng lượng - Khoáng sản'}, {'id': 21, 'name': 'Y tế - Chăm sóc sức khỏe'},
            {'id': 22, 'name': 'Nhân sự'}, {'id': 23, 'name': 'Bảo hiểm'},
            {'id': 24, 'name': 'Thông tin - Truyền thông - Xuất bản - In ấn'}, {'id': 25, 'name': 'Pháp Lý - Tuân thủ'},
            {'id': 26, 'name': 'Kiểm toán'}, {'id': 27, 'name': 'Quản lý dự án - Chương trình'},
            {'id': 28, 'name': 'Quản lý tiêu chuẩn và chất lượng'}, {'id': 29, 'name': 'Bất động sản'},
            {'id': 30, 'name': 'Chăm sóc khách hàng'}, {'id': 31, 'name': 'Xây dựng'},
            {'id': 32, 'name': 'Giáo dục - Đào tạo'},
            {'id': 33, 'name': 'Data Analytics - Warehousing, & Business Intelligence'},
            {'id': 34, 'name': 'Khoa học - Kỹ thuật'}, {'id': 35, 'name': 'Nghề nghiệp khác'}]
    for c in nghe:
        career = Career.objects.create(name=c["name"])
        data[c["id"]] = career.id

    with open("C:/Users/khuy2/Desktop/map.json", "w", encoding="utf-8") as file:
        json.dump({
            "career_map": data
        }, file, ensure_ascii=False)
    return var_res.response_data(data="OKE")


@api_view(http_method_names=["GET"])
def get_all_config(request):
    try:
        # system
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
        job_post_status_tuple = utils.convert_tuple_or_list_to_options(var_sys.JOB_POST_STATUS)

        # database
        cities = City.objects.exclude(name__icontains="Toàn quốc").values_list("id", "name")
        careers = Career.objects.values_list("id", "name")
        city_tuple = utils.convert_tuple_or_list_to_options(cities)
        career_tuple = utils.convert_tuple_or_list_to_options(careers)

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
        job_post_status_options = job_post_status_tuple[0]

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
        job_post_status_dict = job_post_status_tuple[1]

        res_data = {
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
            "jobPostStatusOptions": job_post_status_options,

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
            "jobPostStatusDict": job_post_status_dict
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
