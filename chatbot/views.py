"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from configs import variable_system as var_sys
from chatbot.chat_responses.job_seeker_chat_response import JobSeekerChatResponse
from chatbot.chat_responses.employer_chat_response import EmployerChatResponse


class JobSeekerDialogFlowWebhookView(APIView):
    search_job_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "viec-lam"
    search_company_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "cong-ty"
    manage_profile_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "bang-dieu-khien/ho-so"
    online_profile_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "bang-dieu-khien/ho-so-tung-buoc/resume"
    track_application_status_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "bang-dieu-khien/viec-lam-cua-toi/?tab=2"
    login_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "dang-nhap"
    job_notification_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "bang-dieu-khien/thong-bao"
    faq_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "cau-hoi-thuong-gap"
    how_to_use_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "huong-dan-su-dung"
    account_and_password_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "bang-dieu-khien/tai-khoan"
    about_us_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "ve-chung-toi"
    privacy_policy_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "chinh-sach-bao-mat"
    terms_of_use_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "dieu-khoan-su-dung"
    intellectual_property_link = settings.WEB_JOB_SEEKER_CLIENT_URL + "quyen-so-huu-tri-tue"

    def __init__(self):
        self.job_seeker_chat_response = JobSeekerChatResponse()
    
    def post(self, request):
        try:
            req = request.data
            intent = req.get("queryResult", {}).get("intent", {}).get("displayName")
            if not intent:
                return Response(
                    status=status.HTTP_200_OK, 
                    data=self.job_seeker_chat_response.get_error_intent_response()
                )

            if intent == JobSeekerChatResponse.WELCOME_INTENT:
                res = self.handle_welcome_intent(request)
            elif intent == JobSeekerChatResponse.SEARCH_JOB_INTENT:
                res = self.handle_search_job_intent(request)
            elif intent == JobSeekerChatResponse.SEARCH_COMPANY_INTENT:
                res = self.handle_search_company_intent(request)
            elif intent == JobSeekerChatResponse.MANAGE_PROFILE_INTENT:
                res = self.handle_manage_profile_intent(request)
            elif intent == JobSeekerChatResponse.TRACK_APPLICATION_STATUS_INTENT:
                res = self.handle_track_application_status_intent(request)
            elif intent == JobSeekerChatResponse.FEEDBACK_INTENT:
                res = self.handle_feedback_intent(request)
            elif intent == JobSeekerChatResponse.JOB_NOTIFICATION_INTENT:
                res = self.handle_job_notification_intent(request)
            elif intent == JobSeekerChatResponse.SUPPORT_INTENT:
                res = self.handle_support_intent(request)
            elif intent == JobSeekerChatResponse.CONTACT_CONSULTANT_INTENT:
                res = self.handle_contact_consultant_intent(request)
            elif intent == JobSeekerChatResponse.CONTACT_CONSULTANT_INPUT_NAME_EMAIL_PHONE_INTENT:
                res = self.handle_contact_consultant_input_name_email_phone_intent(request)
            elif intent == JobSeekerChatResponse.ACCOUNT_AND_PASSWORD_INTENT:
                res = self.handle_account_and_password_intent(request)
            elif intent == JobSeekerChatResponse.ABOUT_US_INTENT:
                res = self.handle_about_us_intent(request)
            else:
                res = self.job_seeker_chat_response.get_fallback_intent_response()

            return Response(status=status.HTTP_200_OK, data=res)
        except Exception as e:
            print(f"[JobSeekerDialogFlowWebhookView] Error when processing: {e}")
            res = self.job_seeker_chat_response.get_error_intent_response()
            return Response(status=status.HTTP_200_OK, data=res)

    def handle_welcome_intent(self, request):
        """
        Handle welcome intent
        """
        return self.job_seeker_chat_response.get_welcome_intent_response()
    
    def handle_search_job_intent(self, request):
        """
        Handle search job intent
        """
        return self.job_seeker_chat_response.get_search_job_intent_response(params={
            "search_job_link": self.search_job_link
        })
    
    def handle_search_company_intent(self, request): 
        """
        Handle search company intent
        """
        return self.job_seeker_chat_response.get_search_company_intent_response(params={
            "search_company_link": self.search_company_link
        })
    
    def handle_manage_profile_intent(self, request):
        """
        Handle manage profile intent
        """
        return self.job_seeker_chat_response.get_manage_profile_intent_response(params={
            "manage_profile_link": self.manage_profile_link,
            "online_profile_link": self.online_profile_link
        })
    
    def handle_track_application_status_intent(self, request):
        """
        Handle track application status intent
        """
        return self.job_seeker_chat_response.get_track_application_status_intent_response(params={
            "track_application_status_link": self.track_application_status_link
        })
    
    def handle_feedback_intent(self, request):
        """
        Handle feedback intent
        """
        reference_image_url = var_sys.ABOUT_US_IMAGE_URLS.get("JOB_SEEKER", {}).get("FEEDBACK_GUIDE", "")

        return self.job_seeker_chat_response.get_feedback_intent_response(params={
            "reference_image_url": reference_image_url,
            "login_link": self.login_link
        })
        
    def handle_job_notification_intent(self, request):
        """
        Handle job notification intent
        """
        return self.job_seeker_chat_response.get_job_notification_intent_response(params={
            "job_notification_link": self.job_notification_link,
            "login_link": self.login_link
        })
    
    def handle_support_intent(self, request):
        """
        Handle support intent
        """
        return self.job_seeker_chat_response.get_support_intent_response(params={
            "faq_link": self.faq_link,
            "how_to_use_link": self.how_to_use_link
        })
    
    def handle_contact_consultant_intent(self, request):
        """
        Handle contact consultant intent
        """
        return self.job_seeker_chat_response.get_contact_consultant_intent_response()
    
    def handle_contact_consultant_input_name_email_phone_intent(self, request):
        """
        Handle contact consultant input name email phone intent
        """
        # Define output context name
        output_context_name = '/contactinfo'
        # Get data from request
        data = request.data
        query_result = data.get('queryResult', {})
        # Get contact consultant info from query result
        contact_consultant_info = self.__get_contact_consultant_info(query_result, output_context_name)
        # If contact consultant info is not found, return error intent response 
        if not contact_consultant_info:
            return self.job_seeker_chat_response.get_error_intent_response()
        
        # If contact consultant info is found, return contact consultant input name email phone intent response
        return self.job_seeker_chat_response.get_contact_consultant_input_name_email_phone_intent_response(params={
            "name": contact_consultant_info.get('name.original', '---'),
            "email": contact_consultant_info.get('email.original', '---'),
            "phone": contact_consultant_info.get('phone.original', '---')
        })
    
    def handle_account_and_password_intent(self, request):
        """
        Handle account and password intent
        """
        return self.job_seeker_chat_response.get_account_and_password_intent_response(params={
            "account_and_password_link": self.account_and_password_link,
            "faq_link": self.faq_link,
            "how_to_use_link": self.how_to_use_link
        })  
    
    def handle_about_us_intent(self, request):
        """
        Handle about us intent
        """
        params = {
            "about_us_company_count": "20.000+",
            "about_us_job_count": "1.000.000+",
            "about_us_candidate_count": "5.000.000+",
            "about_us_satisfaction_rate": "98%",
            "about_us_matching_rate": "95%",
            "about_us_image_url": var_sys.ABOUT_US_IMAGE_URLS.get("JOB_SEEKER", {}).get("ACHIEVEMENTS", ""),
            "about_us_action_link": "",
            "search_company_link": self.search_company_link,
            "search_job_link": self.search_job_link,
            "google_play_download_app_link": var_sys.LINK_GOOGLE_PLAY,
            "app_store_download_app_link": var_sys.LINK_APPSTORE,
            "about_us_contact_info": [
                f'🏙️ Địa chỉ: {var_sys.COMPANY_INFO.get("ADDRESS", "")}',
                f'☎️ Hotline: {var_sys.COMPANY_INFO.get("PHONE", "")}',
                f'✉️ Email: {var_sys.COMPANY_INFO.get("EMAIL", "")}',
                f'⏰ Giờ làm việc: {var_sys.COMPANY_INFO.get("WORK_TIME", "")}'
            ],
            "facebook_link": var_sys.SOCIAL_MEDIA_LINKS.get("facebook"),
            "linkedin_link": var_sys.SOCIAL_MEDIA_LINKS.get("linkedin"),
            "youtube_link": var_sys.SOCIAL_MEDIA_LINKS.get("youtube"),
            "instagram_link": var_sys.SOCIAL_MEDIA_LINKS.get("instagram"),
            "privacy_policy_link": self.privacy_policy_link,
            "terms_of_use_link": self.terms_of_use_link,
            "intellectual_property_link": self.intellectual_property_link
        }
        return self.job_seeker_chat_response.get_about_us_intent_response(params=params)
    
    def __get_contact_consultant_info(self, query_result, output_context_name):
        """
        Get contact consultant info from query result
        """
        output_contexts = query_result.get('outputContexts', [])
        contact_consultant_info_output_context = next((context for context in output_contexts if context.get('name', '').endswith(output_context_name)), None)
        if contact_consultant_info_output_context:
            parameters = contact_consultant_info_output_context.get('parameters', {})

            return parameters
        return None

class EmployerDialogFlowWebhookView(APIView):
    search_candidate_link = settings.WEB_EMPLOYER_CLIENT_URL + "danh-sach-ung-vien"
    manage_candidate_link = settings.WEB_EMPLOYER_CLIENT_URL + "ho-so-ung-tuyen"
    update_company_info_link = settings.WEB_EMPLOYER_CLIENT_URL + "cong-ty"
    faq_link = settings.WEB_EMPLOYER_CLIENT_URL + "cau-hoi-thuong-gap"
    how_to_use_link = settings.WEB_EMPLOYER_CLIENT_URL + "huong-dan-su-dung"
    account_and_password_link = settings.WEB_EMPLOYER_CLIENT_URL + "tai-khoan"
    privacy_policy_link = settings.WEB_EMPLOYER_CLIENT_URL + "chinh-sach-bao-mat"
    terms_of_use_link = settings.WEB_EMPLOYER_CLIENT_URL + "dieu-khoan-su-dung"
    intellectual_property_link = settings.WEB_EMPLOYER_CLIENT_URL + "quyen-so-huu-tri-tue"

    def __init__(self):
        self.employer_chat_response = EmployerChatResponse()

    def post(self, request):
        try:
            req = request.data
            intent = req.get("queryResult", {}).get("intent", {}).get("displayName")
            if not intent:
                return Response(
                    status=status.HTTP_200_OK, 
                    data=self.employer_chat_response.get_error_intent_response()
                )

            if intent == EmployerChatResponse.WELCOME_INTENT:
                res = self.handle_welcome_intent(request)
            elif intent == EmployerChatResponse.SEARCH_CANDIDATE_INTENT:
                res = self.handle_search_candidate_intent(request)
            elif intent == EmployerChatResponse.MANAGE_CANDIDATE_INTENT:
                res = self.handle_manage_candidate_intent(request)
            elif intent == EmployerChatResponse.UPDATE_COMPANY_INFO_INTENT:
                res = self.handle_update_company_info_intent(request)
            elif intent == EmployerChatResponse.FEEDBACK_INTENT:
                res = self.handle_feedback_intent(request)
            elif intent == EmployerChatResponse.SUPPORT_INTENT:
                res = self.handle_support_intent(request)
            elif intent == EmployerChatResponse.CONTACT_CONSULTANT_INTENT:
                res = self.handle_contact_consultant_intent(request)
            elif intent == EmployerChatResponse.CONTACT_CONSULTANT_INPUT_NAME_COMPANY_EMAIL_PHONE_INTENT:
                res = self.handle_contact_consultant_input_name_company_email_phone_intent(request)
            elif intent == EmployerChatResponse.ACCOUNT_AND_PASSWORD_INTENT:
                res = self.handle_account_and_password_intent(request)
            elif intent == EmployerChatResponse.ABOUT_US_INTENT:
                res = self.handle_about_us_intent(request)
            else:
                res = self.employer_chat_response.get_fallback_intent_response()

            return Response(status=status.HTTP_200_OK, data=res)
        except Exception as e:
            print(f"[EmployerDialogFlowWebhookView] Error when processing: {e}")
            res = self.employer_chat_response.get_error_intent_response()
            return Response(status=status.HTTP_200_OK, data=res)

    def handle_welcome_intent(self, request):
        """
        Handle welcome intent
        """
        return self.employer_chat_response.get_welcome_intent_response()
    
    def handle_search_candidate_intent(self, request):
        """
        Handle search candidate intent
        """
        return self.employer_chat_response.get_search_candidate_intent_response(params={
            "search_candidate_link": self.search_candidate_link
        })  
    
    def handle_manage_candidate_intent(self, request):
        """
        Handle manage candidate intent
        """
        return self.employer_chat_response.get_manage_candidate_intent_response(params={
            "manage_candidate_link": self.manage_candidate_link
        })
    
    def handle_update_company_info_intent(self, request):
        """
        Handle update company info intent
        """
        return self.employer_chat_response.get_update_company_info_intent_response(params={
            "update_company_info_link": self.update_company_info_link
        })
    
    def handle_feedback_intent(self, request):
        """
        Handle feedback intent
        """
        feedback_image_url = f"https://img.icons8.com/?size=100&id=52209&format=png"
        return self.employer_chat_response.get_feedback_intent_response(params={
            "feedback_image_url": feedback_image_url
        })  
    
    def handle_support_intent(self, request):
        """
        Handle support intent
        """
        return self.employer_chat_response.get_support_intent_response(params={
            "faq_link": self.faq_link,
            "how_to_use_link": self.how_to_use_link
        })
    
    def handle_contact_consultant_intent(self, request):
        """
        Handle contact consultant intent
        """
        return self.employer_chat_response.get_contact_consultant_intent_response()
    
    def handle_contact_consultant_input_name_company_email_phone_intent(self, request):
        """
        Handle contact consultant input name company email phone intent
        """
        # Define output context name
        output_context_name = '/contactinfo'
        # Get data from request
        data = request.data
        query_result = data.get('queryResult', {})
        # Get contact consultant info from query result
        contact_consultant_info = self.__get_contact_consultant_info(query_result, output_context_name)
        # If contact consultant info is not found, return error intent response 
        if not contact_consultant_info:
            return self.employer_chat_response.get_error_intent_response()
        # If contact consultant info is found, return contact consultant input name company email phone intent response
        return self.employer_chat_response.get_contact_consultant_input_name_company_email_phone_intent_response(params={
            "name": contact_consultant_info.get('name.original', '---'),
            "company_name": contact_consultant_info.get('company_name.original', '---'),
            "email": contact_consultant_info.get('email.original', '---'),
            "phone": contact_consultant_info.get('phone.original', '---')
        })
    
    def handle_account_and_password_intent(self, request):
        """
        Handle account and password intent
        """
        return self.employer_chat_response.get_account_and_password_intent_response(params={
            "account_and_password_link": self.account_and_password_link,
            "faq_link": self.faq_link,
            "how_to_use_link": self.how_to_use_link
        })
    
    def handle_about_us_intent(self, request):
        """
        Handle about us intent
        """
        params = {
            "about_us_company_count": "20.000+",
            "about_us_job_count": "1.000.000+",
            "about_us_candidate_count": "5.000.000+",
            "about_us_satisfaction_rate": "98%",
            "about_us_matching_rate": "95%",
            "about_us_image_url": var_sys.ABOUT_US_IMAGE_URLS.get("EMPLOYER", {}).get("ACHIEVEMENTS", ""),
            "about_us_action_link": "",
            "search_candidate_link": self.search_candidate_link,
            "google_play_download_app_link": var_sys.LINK_GOOGLE_PLAY,
            "app_store_download_app_link": var_sys.LINK_APPSTORE,
            "about_us_contact_info": [
                f'🏙️ Địa chỉ: {var_sys.COMPANY_INFO.get("ADDRESS", "")}',
                f'☎️ Hotline: {var_sys.COMPANY_INFO.get("PHONE", "")}',
                f'✉️ Email: {var_sys.COMPANY_INFO.get("EMAIL", "")}',
                f'⏰ Giờ làm việc: {var_sys.COMPANY_INFO.get("WORK_TIME", "")}'
            ],
            "facebook_link": var_sys.SOCIAL_MEDIA_LINKS.get("facebook"),
            "linkedin_link": var_sys.SOCIAL_MEDIA_LINKS.get("linkedin"),
            "youtube_link": var_sys.SOCIAL_MEDIA_LINKS.get("youtube"),
            "instagram_link": var_sys.SOCIAL_MEDIA_LINKS.get("instagram"),
            "privacy_policy_link": self.privacy_policy_link,
            "terms_of_use_link": self.terms_of_use_link,
            "intellectual_property_link": self.intellectual_property_link
        }
        return self.employer_chat_response.get_about_us_intent_response(params=params)
    
    def __get_contact_consultant_info(self, query_result, output_context_name):
        """
        Get contact consultant info from query result
        """
        output_contexts = query_result.get('outputContexts', [])
        contact_consultant_info_output_context = next((context for context in output_contexts if context.get('name', '').endswith(output_context_name)), None)
        if contact_consultant_info_output_context:
            parameters = contact_consultant_info_output_context.get('parameters', {})

            return parameters
        return None