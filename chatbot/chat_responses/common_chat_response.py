"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from django.conf import settings
from configs.variable_system import (JOB_SEEKER, EMPLOYER, CHATBOT_ICONS)


class CommonChatResponse:
    def __init__(self):
        self.app_name = settings.COMPANY_NAME
        self.chatbot_icons = CHATBOT_ICONS

    def _get_text_response_component(self, text: list[str] = []):
        """
        Return response with text component

        Args:
            text (list[str]): Text of text component

        Returns:
            dict: Text component
        """
        return {
            "text": {
                "text": text
            }
        }

    def _get_info_response_component(self, title: str = "", subtitle: str = "", image_url: str = "", action_link: str = ""):
        """
        Return response with info component

        Args:
            title (str): Title of info component
            subtitle (str): Subtitle of info component
            image_url (str): Image url of info component
            action_link (str): Action link of info component

        Returns:
            dict: Info component
        """
        return {
            "type": "info",
            "title": title,
            "subtitle": subtitle,
            "image": {
                "src": {
                    "rawUrl": image_url
                }
            },
            "actionLink": action_link
        }

    def _get_description_response_component(self, title: str = "", text: list[str] = []):
        """
        Return response with description component

        Args:
            title (str): Title of description component
            text (list[str]): Text of description component

        Returns:
            dict: Description component
        """
        return {
            "type": "description",
            "title": title,
            "text": text
        }

    def _get_image_response_component(self, image_url: str = "", accessibility_text: str = ""):
        """
        Return response with image component

        Args:
            image_url (str): Image url of image component
            accessibility_text (str): Accessibility text of image component

        Returns:
            dict: Image component
        """
        return {
            "type": "image",
            "rawUrl": image_url,
            "accessibilityText": accessibility_text
        }

    def _get_button_response_component(self, text: str = "", link: str = "", icon_type: str = "", icon_color: str = "", event: dict = {}):
        """
        Return response with button component

        Args:
            text (str): Text of button component
            link (str): Link of button component
            icon_type (str): Type of icon of button component
            icon_color (str): Color of icon of button component
            event (dict): Event of button component

        Returns:
            dict: Button component
        """
        return {
            "type": "button",
            "icon": {
                "type": icon_type,
                "color": icon_color
            },
            "text": text,
            "link": link,
            "event": event
        }

    def _get_divider_response_component(self):
        """
        Return response with divider component

        Returns:
            dict: Divider component
        """
        return {
            "type": "divider"
        }

    def _get_list_item_response_component(self, title: str = "", subtitle: str = "", event: dict = {}):
        """
        Return response with list item component

        Args:
            title (str): Title of list item component
            subtitle (str): Subtitle of list item component
            event (dict): Event of list item component

        Returns:
            dict: List item component
        """
        return {
            "type": "list",
            "title": title,
            "subtitle": subtitle,
            "event": event
        }

    def _get_accordion_response_component(self, title: str = "", subtitle: str = "", image_url: str = "", text: str = ""):
        """
        Return response with accordion component

        Args:
            title (str): Title of accordion component
            subtitle (str): Subtitle of accordion component
            image_url (str): Image url of accordion component
            text (str): Text of accordion component

        Returns:
            dict: Accordion component
        """
        return {
            "type": "accordion",
            "title": title,
            "subtitle": subtitle,
            "image": {
                "src": {
                    "rawUrl": image_url
                }
            },
            "text": text
        }

    def _get_suggestion_chip_response_component(self, options: list[dict] = []):
        """
        Return response with suggestion chip component

        Args:
            options (list[dict]): List of options for suggestion chip component

        Returns:
            dict: Suggestion chip component
        """
        options = [
            {
                "text": item.get("text", ""),
                "link": item.get("link", ""),
                "image": {
                    "src": {
                        "rawUrl": item.get("icon_url", "")
                    }
                }
            }
            for item in options
        ]
        return {
            "type": "chips",
            "options": options
        }

    def get_fallback_intent_response(self):
        """
        Return response for FallbackIntent
        """
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        "Xin lỗi, tôi không hiểu ý bạn là gì. Vui lòng thử lại."
                    ]
                )
            ]
        }

    def get_error_intent_response(self, error_message=None):
        """
        Return response for ErrorIntent
        """
        if error_message is None:
            error_message = "Đã xảy ra lỗi. Vui lòng thử lại."
        return {
            "fulfillmentMessages": [
                self._get_text_response_component(
                    text=[
                        error_message
                    ]
                )
            ]
        }
