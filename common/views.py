from configs import variable_system as var_sys
from helpers import utils, helper
from configs import variable_response as var_res
from rest_framework.decorators import api_view
from rest_framework import status


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

