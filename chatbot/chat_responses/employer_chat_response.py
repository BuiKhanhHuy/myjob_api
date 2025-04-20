"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from chatbot.chat_responses.common_chat_response import CommonChatResponse


class EmployerChatResponse(CommonChatResponse):
    WELCOME_INTENT = "WelcomeIntent"
    SEARCH_CANDIDATE_INTENT = "SearchCandidateIntent"
    MANAGE_CANDIDATE_INTENT = "ManageCandidateIntent"
    UPDATE_COMPANY_INFO_INTENT = "UpdateCompanyInfoIntent"
    FEEDBACK_INTENT = "FeedbackIntent"
    SUPPORT_INTENT = "SupportIntent"
    CONTACT_CONSULTANT_INTENT = "ContactConsultantIntent"
    CONTACT_CONSULTANT_INPUT_NAME_COMPANY_EMAIL_PHONE_INTENT = "ContactConsultant_InputName_CompanyName_Email_Phone_Intent"
    ACCOUNT_AND_PASSWORD_INTENT = "AccountAndPasswordIntent"
    ABOUT_US_INTENT = "AboutUsIntent"
    
    def __init__(self):
        super().__init__()

    def get_welcome_intent_response(self, params={}):
        """
        Return response with list of chip options for WelcomeIntent
        
        Args:
            params (dict): Dictionary of parameters

        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        f"Xin chào! Mình là trợ lý tuyển dụng của {self.app_name}. Mình có thể giúp gì cho bạn? 👋"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(options=[
                                    {"text": "Tìm kiếm ứng viên",
                                        "icon_url": self.chatbot_icons["employer_search_candidate"]},
                                    {"text": "Hồ sơ ứng tuyển",
                                        "icon_url": self.chatbot_icons["employer_manage_candidate"]},
                                    {"text": "Cập nhật thông tin công ty",
                                        "icon_url": self.chatbot_icons["employer_update_company_info"]},
                                    {"text": "Đánh giá và phản hồi",
                                        "icon_url": self.chatbot_icons["common_feedback"]},
                                    {"text": "Hỗ trợ",
                                        "icon_url": self.chatbot_icons["common_support"]},
                                    {"text": "Về chúng tôi",
                                        "icon_url": self.chatbot_icons["common_about_us"]},
                                ])
                            ]
                        ]
                    }
                },
                self._get_text_response_component(
                    text=["Không biết bạn cần hỗ trợ gì về tuyển dụng ha? 😊"]
                )
            ]
        }

    def get_search_candidate_intent_response(self, params={}):
        """
        Return response for SearchCandidateIntent
        
        Args:
            params (dict): Dictionary of parameters
                search_candidate_link: str - link to search candidate page
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        "Bạn có thể nhấn vào nút bên dưới để tìm kiếm ứng viên phù hợp nha! 🥳"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Đi đến trang tìm kiếm ứng viên",
                                            "image_url": self.chatbot_icons["employer_search_candidate"],
                                            "link": params.get("search_candidate_link", "")
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                },
                self._get_text_response_component(
                    text=[
                        "Không biết bạn cần mình hỗ trợ gì thêm về tuyển dụng không ha? 🤗"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "image_url": self.chatbot_icons["employer_manage_candidate"],
                                            "text": "Hồ sơ ứng tuyển"
                                        },
                                        {
                                            "text": "Cập nhật thông tin công ty",
                                            "image_url": self.chatbot_icons["employer_update_company_info"]
                                        },
                                        {
                                            "text": "Đánh giá và phản hồi",
                                            "image_url": self.chatbot_icons["common_feedback"]
                                        },
                                        {
                                            "text": "Hỗ trợ",
                                            "image_url": self.chatbot_icons["common_support"]
                                        },
                                        {
                                            "text": "Về chúng tôi",
                                            "image_url": self.chatbot_icons["common_about_us"]
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                }
            ]
        }

    def get_manage_candidate_intent_response(self, params={}):
        """
        Return response for ManageCandidateIntent
        
        Args:
            params (dict): Dictionary of parameters
                manage_candidate_link: str - link to manage candidate page
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        "Bạn có thể nhấn vào nút bên dưới để quản lý hồ sơ ứng tuyển nha! 🥳"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(options=[
                                    {
                                        "text": "Đi đến trang quản lý hồ sơ ứng tuyển",
                                        "image_url": self.chatbot_icons["employer_manage_candidate"],
                                        "link": params.get("manage_candidate_link", "")
                                    }
                                ])
                            ]
                        ]
                    }
                },
                self._get_text_response_component(
                    text=[
                        "Không biết bạn cần mình hỗ trợ gì thêm về tuyển dụng không ha? 🤗"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Tìm kiếm ứng viên",
                                            "image_url": self.chatbot_icons["employer_search_candidate"]
                                        },
                                        {
                                            "text": "Cập nhật thông tin công ty",
                                            "image_url": self.chatbot_icons["employer_update_company_info"]
                                        },
                                        {
                                            "text": "Đánh giá và phản hồi",
                                            "image_url": self.chatbot_icons["common_feedback"]
                                        },
                                        {
                                            "text": "Hỗ trợ",
                                            "image_url": self.chatbot_icons["common_support"]
                                        },
                                        {
                                            "text": "Về chúng tôi",
                                            "image_url": self.chatbot_icons["common_about_us"]
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                }
            ]
        }

    def get_update_company_info_intent_response(self, params={}):
        """
        Return response for UpdateCompanyInfoIntent
        
        Args:
            params (dict): Dictionary of parameters
                update_company_info_link: str - link to update company info page
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        "Bạn có thể nhấn vào nút bên dưới để cập nhật thông tin công ty nha! 🥳"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(options=[
                                    {
                                        "text": "Cập nhật thông tin công ty",
                                        "image_url": self.chatbot_icons["employer_update_company_info"],
                                        "link": params.get("update_company_info_link", "")
                                    }
                                ])
                            ]
                        ]
                    }
                },
                self._get_text_response_component(
                    text=[
                        "Không biết bạn cần mình hỗ trợ gì thêm về tuyển dụng không ha? 🤗"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Tìm kiếm ứng viên",
                                            "image_url": self.chatbot_icons["employer_search_candidate"]
                                        },
                                        {
                                            "text": "Hồ sơ ứng tuyển",
                                            "image_url": self.chatbot_icons["employer_manage_candidate"]
                                        },
                                        {
                                            "text": "Đánh giá và phản hồi",
                                            "image_url": self.chatbot_icons["common_feedback"]
                                        },
                                        {
                                            "text": "Hỗ trợ",
                                            "image_url": self.chatbot_icons["common_support"]
                                        },
                                        {
                                            "text": "Về chúng tôi",
                                            "image_url": self.chatbot_icons["common_about_us"]
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                }
            ]
        }

    def get_feedback_intent_response(self, params={}):
        """
        Return response for FeedbackIntent
        
        Args:
            params (dict): Dictionary of parameters
                feedback_image_url: str - image url
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        'Bạn có thể nhấn vào nút "Phản hồi" ở góc dưới bên trái để đánh giá và phản hồi về dịch vụ của MyJob!'
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_image_response_component(
                                    image_url=params.get("feedback_image_url", ""),
                                    accessibility_text="Description image"
                                )
                            ]
                        ]
                    }
                },
                self._get_text_response_component(
                    text=[
                        "Không biết bạn cần mình hỗ trợ gì thêm về tuyển dụng không ha? 🤗"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Tìm kiếm ứng viên",
                                            "image_url": self.chatbot_icons["employer_search_candidate"]
                                        },
                                        {
                                            "text": "Hồ sơ ứng tuyển",
                                            "image_url": self.chatbot_icons["employer_manage_candidate"]
                                        },
                                        {
                                            "text": "Cập nhật thông tin công ty",
                                            "image_url": self.chatbot_icons["employer_update_company_info"]
                                        },
                                        {
                                            "text": "Đánh giá và phản hồi",
                                            "image_url": self.chatbot_icons["common_feedback"]
                                        },
                                        {
                                            "text": "Hỗ trợ",
                                            "image_url": self.chatbot_icons["common_support"]
                                        },
                                        {
                                            "text": "Về chúng tôi",
                                            "image_url": self.chatbot_icons["common_about_us"]
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                }
            ]
        }

    def get_support_intent_response(self, params={}):
        """
        Return response for SupportIntent
        
        Args:
            params (dict): Dictionary of parameters
                faq_link: str - link to faq page
                how_to_use_link: str - link to how to use page
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Mình có thể giúp gì cho bạn về tuyển dụng không? Hãy cho mình biết bạn đang gặp vấn đề gì nhé! 😊"
                        ]
                    }
                },
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Tài khoản & Mật khẩu",
                                            "icon_url": self.chatbot_icons["common_account_and_password"]
                                        },
                                        {
                                            "text": "Câu hỏi thường gặp",
                                            "icon_url": self.chatbot_icons["common_faq"],
                                            "link": params.get("faq_link", "")
                                        },
                                        {
                                            "text": "Hướng dẫn sử dụng",
                                            "icon_url": self.chatbot_icons["common_how_to_use"],
                                            "link": params.get("how_to_use_link", "")
                                        },
                                        {
                                            "text": "Liên hệ trực tiếp với tư vấn viên",
                                            "icon_url": self.chatbot_icons["common_chat_with_us"]
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                }
            ]
        }

    def get_contact_consultant_intent_response(self, params={}):
        """
        Return response for ContactConsultantIntent
        
        Args:
            params (dict): Dictionary of parameters

        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        "Để tư vấn viên có thể hỗ trợ bạn tốt nhất về tuyển dụng, mình cần bạn cung cấp một vài thông tin nhé! 😊",
                        "Đầu tiên, bạn cho mình biết tên của bạn được không ạ? 👋",
                    ]
                )
            ]
        }

    def get_contact_consultant_input_name_company_email_phone_intent_response(self, params={}):
        """
        Return response for ContactConsultant_InputName_CompanyName_Email_Phone_Intent
        
        Args:
            params (dict): Dictionary of parameters
                name: str - name
                company: str - company
                email: str - email
                phone: str - phone
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_description_response_component(
                                    title="Thông tin liên hệ của bạn",
                                    text=[
                                        "➤ Tên: " + params.get("name", ""),
                                        "➤ Tên công ty: " + params.get("company_name", ""),
                                        "➤ Email: " + params.get("email", ""),
                                        "➤ Số điện thoại: " + params.get("phone", ""),
                                    ]
                                )
                            ]
                        ]
                    }
                },
                self._get_text_response_component(
                    text=[
                        "Cảm ơn bạn rất nhiều! Tư vấn viên của chúng tôi sẽ liên hệ với bạn trong thời gian sớm nhất. 🙏"
                    ]
                )
            ]
        }

    def get_account_and_password_intent_response(self, params={}):
        """
        Return response for AccountAndPasswordIntent
        
        Args:
            params (dict): Dictionary of parameters
                account_and_password_link: str - link to account and password page
                faq_link: str - link to faq page
                how_to_use_link: str - link to how to use page
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Nhấp vào nút bên dưới để vào trang tài khoản và mật khẩu của bạn nha! 😊"
                        ]
                    }
                },
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Đi đến trang tài khoản và mật khẩu",
                                            "icon_url": self.chatbot_icons["common_account_and_password"],
                                            "link": params.get("account_and_password_link", "")
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                },
                self._get_text_response_component(
                    text=[
                        f"Bạn còn cần {self.app_name} hỗ trợ gì về tuyển dụng nữa không nè? Đừng ngại chia sẻ với mình nhé! 🤗"
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Câu hỏi thường gặp",
                                            "icon_url": self.chatbot_icons["common_faq"],
                                            "link": params.get("faq_link", "")
                                        },
                                        {
                                            "text": "Hướng dẫn sử dụng",
                                            "icon_url": self.chatbot_icons["common_how_to_use"],
                                            "link": params.get("how_to_use_link", "")
                                        },
                                        {
                                            "text": "Liên hệ trực tiếp với tư vấn viên",
                                            "icon_url": self.chatbot_icons["common_chat_with_us"]
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                }
            ]
        }

    def get_about_us_intent_response(self, params={}):
        """
        Return response for AboutUsIntent
        
        Args:
            params (dict): Dictionary of parameters
                about_us_company_count: str - number of companies
                about_us_job_count: str - number of jobs
                about_us_candidate_count: str - number of candidates
                about_us_satisfaction_rate: str - satisfaction rate
                about_us_matching_rate: str - matching rate
                about_us_image_url: str - image url
                about_us_action_link: str - action link
                search_candidate_link: str - link to search candidate page
                google_play_download_app_link: str - link to google play download app
                app_store_download_app_link: str - link to app store download app
                about_us_contact_info: list[str] - contact info
                facebook_link: str - link to facebook
                linkedin_link: str - link to linkedin
                youtube_link: str - link to youtube
                instagram_link: str - link to instagram
                privacy_policy_link: str - link to privacy policy
                terms_of_use_link: str - link to terms of use
                intellectual_property_link: str - link to intellectual property
        Returns:
            dict: Response with list of chip options
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        f"🌟 CHÀO MỪNG BẠN ĐẾN VỚI {self.app_name.upper()} 🌟",
                        f'{self.app_name} - Kênh thông tin tuyển dụng và việc làm dành cho mọi Doanh nghiệp và Ứng viên. ',
                        'Chúng tôi tin tưởng sẽ đem lại "HY VỌNG" cho Doanh nghiệp tìm kiếm nhân tài và cho Ứng viên tìm kiếm cơ hội nghề nghiệp.',
                        f'Với 2 hệ thống: Website dành cho Nhà Tuyển Dụng và Ứng dụng (Application) dành cho Người Tìm Việc, {self.app_name} sẽ mang lại những trải nghiệm mới mẻ, thú vị; kết nối ước mơ chinh phục công việc của mọi nhân tài và giúp doanh nghiệp xây dựng đội ngũ nhân sự vững mạnh.'
                    ]
                ),
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_info_response_component(
                                    title="Chọn đúng việc - Đi đúng hướng",
                                    subtitle="Khám phá công việc phù hợp với định hướng nghề nghiệp. Thông tin chi tiết về yêu cầu công việc, môi trường và cơ hội phát triển tại mỗi công ty.",
                                    image_url=self.chatbot_icons.get("job_seeker_about_us_target_1", ""),
                                ),
                                self._get_info_response_component(
                                    title="Tạo CV & Profile",
                                    subtitle="Xây dựng hồ sơ ứng tuyển chuyên nghiệp với công cụ tạo CV thông minh. Tối ưu profile với các mẫu CV đẹp mắt theo từng ngành nghề.",
                                    image_url=self.chatbot_icons.get("job_seeker_about_us_target_2", "")
                                ),
                                self._get_info_response_component(
                                    title="Việc làm xung quanh bạn",
                                    subtitle="Tìm kiếm cơ hội việc làm lý tưởng trong khu vực. Với tính năng định vị thông minh, gợi ý công việc phù hợp gần nơi bạn sinh sống.",
                                    image_url=self.chatbot_icons.get("job_seeker_about_us_target_3", "")
                                ),
                                self._get_info_response_component(
                                    title="Thông báo việc làm mọi lúc",
                                    subtitle="Không bỏ lỡ cơ hội với hệ thống thông báo thông minh. Nhận thông tin tức thì về các vị trí việc làm mới phù hợp với kỹ năng.",
                                    image_url=self.chatbot_icons.get("job_seeker_about_us_target_4", "")
                                )
                            ]
                        ]
                    }
                },
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_description_response_component(
                                    title=f"💫 {self.app_name.upper()} - CON SỐ ẤN TƯỢNG:",
                                    text=[
                                        f"🏢 {params.get('about_us_company_count', '')} Doanh nghiệp đối tác",
                                        f"💼 {params.get('about_us_job_count', '')} Việc làm mỗi năm",
                                        f"👥 {params.get('about_us_candidate_count', '')} Ứng viên tin tưởng",
                                        f"🌟 {params.get('about_us_satisfaction_rate', '')} Tỷ lệ hài lòng",
                                        f"🎯 {params.get('about_us_matching_rate', '')} Tỷ lệ matching công việc cao nhất thị trường"
                                    ]
                                )
                            ],
                            [
                                self._get_image_response_component(
                                    image_url=params.get("about_us_image_url", ""),
                                    accessibility_text="Alt image"
                                ),
                                self._get_info_response_component(
                                    title="🏆 THÀNH TỰU NỔI BẬT",
                                    subtitle=[
                                        f"Số 1 về tuyển dụng tại Việt Nam",
                                        f"Tìm kiếm hàng triệu ứng viên chất lượng tại {self.app_name}!"
                                    ],
                                    action_link=params.get("about_us_action_link", "")
                                ),
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Ứng viên nổi bật",
                                            "link": params.get("search_candidate_link", "")
                                        },
                                        {
                                            "text": "Tải ứng dụng trên Google Play",
                                            "link": params.get("google_play_download_app_link", "")
                                        },
                                        {
                                            "text": "Tải ứng dụng trên App Store",
                                            "link": params.get("app_store_download_app_link", "")
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                },
                {
                    "payload": {
                        "richContent": [
                            [
                                self._get_description_response_component(
                                    title="📞 THÔNG TIN LIÊN HỆ:",
                                    text=params.get("about_us_contact_info", "")
                                )
                            ],
                            [
                                self._get_info_response_component(
                                    title="KẾT NỐI VỚI CHÚNG TÔI",
                                    subtitle=f"Theo dõi {self.app_name} trên các nền tảng mạng xã hội để cập nhật thông tin mới nhất về thị trường việc làm và cơ hội nghề nghiệp!",
                                    image_url=self.chatbot_icons.get("common_social", "")
                                ),
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Facebook",
                                            "icon_url": self.chatbot_icons.get("common_social_facebook", ""),
                                            "link": params.get("facebook_link", "")
                                        },
                                        {
                                            "text": "LinkedIn",
                                            "icon_url": self.chatbot_icons.get("common_social_linkedin", ""),
                                            "link": params.get("linkedin_link", "")
                                        },
                                        {
                                            "text": "Youtube",
                                            "icon_url": self.chatbot_icons.get("common_social_youtube", ""),
                                            "link": params.get("youtube_link", "")
                                        },
                                        {
                                            "text": "Instagram",
                                            "icon_url": self.chatbot_icons.get("common_social_instagram", ""),
                                            "link": params.get("instagram_link", "")
                                        }
                                    ]
                                )
                            ],
                            [
                                self._get_info_response_component(
                                    title="CHÍNH SÁCH & ĐIỀU KHOẢN",
                                    subtitle=f"{self.app_name} cam kết bảo vệ quyền lợi và thông tin của người dùng. Vui lòng đọc kỹ các chính sách trước khi sử dụng dịch vụ.",
                                    image_url=self.chatbot_icons.get("common_privacy_policy", "")
                                ),
                                self._get_suggestion_chip_response_component(
                                    options=[
                                        {
                                            "text": "Chính sách bảo mật",
                                            "link": params.get("privacy_policy_link", "")
                                        },
                                        {
                                            "text": "Điều khoản sử dụng",
                                            "link": params.get("terms_of_use_link", "")
                                        },
                                        {
                                            "text": "Quyền sở hữu trí tuệ",
                                            "link": params.get("intellectual_property_link", "")
                                        }
                                    ]
                                )
                            ]
                        ]
                    }
                }
            ]
        }
