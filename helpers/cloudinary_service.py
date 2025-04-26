"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""


import uuid
from cloudinary import uploader as uploader_cloudinary, utils as utils_cloudinary
from helpers import helper

class CloudinaryService:
    @staticmethod
    def upload_image(file, folder: str, public_id: str = None, options: dict = {}):
        """
        Upload image to Cloudinary
        
        Args:
            file: File object
            folder: Folder name
            public_id: Public ID
            options: Options
            
        Returns:
            Upload result
        """
        try:
            upload_result = uploader_cloudinary.upload(
                file,
                folder=folder,
                public_id=public_id if public_id else str(uuid.uuid4()),
                **options
            )
            return upload_result
        except Exception as e:
            helper.print_log_error("cloudinary_upload_image", e)
            return None
    
    @staticmethod
    def delete_image(public_id: str):
        """
        Delete image from Cloudinary
        
        Args:
            public_id: Public ID
            
        Returns:
            Delete result (bool)
        """
        try:
            destroy_result = uploader_cloudinary.destroy(public_id)
            if destroy_result.get("result", "") != "ok":
                raise Exception("Cloudinary delete image failed")
            return True
        except Exception as e:
            helper.print_log_error("cloudinary_delete_image", e)
            return False
    
    @staticmethod
    def get_url_from_public_id(public_id: str, options_config: dict = {}):
        """
        Get URL from public ID
        
        Args:
            public_id: Public ID
            options_config: Options config
            
        Returns:
            URL and options
        """
        try:
            if not public_id:
                return None
                
            # Ensure always use HTTPS
            options_config['secure'] = True
            url, options = utils_cloudinary.cloudinary_url(public_id, **options_config)
            return url, options
            
        except Exception as e:
            helper.print_log_error("cloudinary_get_url", e)
            return None, None