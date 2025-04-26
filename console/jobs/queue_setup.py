"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

import logging
import json
from celery import shared_task
from django.db import transaction
from common.models import File
from helpers.cloudinary_service import CloudinaryService
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

def upload_image(url, folder, options={}):
    """
    Upload image to Cloudinary
    
    Args:
        url: URL of the image
        folder: Folder name
        options: Options
        
    Returns:
        Upload result
    """
    try:
        if "public_id" in options:
            res = CloudinaryService.upload_image(url, folder, public_id=options.get("public_id"))
        else:
            res = CloudinaryService.upload_image(url, folder)
        return res
    except Exception as e:
        raise e
    
def upload_multiple_images(images_data_dict, folder):
    """
    Upload multiple images to Cloudinary
    
    Args:
        images_data_dict: Dictionary of images data
        folder: Folder name
        
    Returns:
        Upload result
    """
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_key = {}
        for key, url in images_data_dict.items():
            future_to_key[executor.submit(upload_image, url, folder, {"public_id": key})] = key 
            
        results = {}
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                uploaded_url = future.result()
                if uploaded_url:
                    results[key] = uploaded_url
            except Exception as e:
                logger.error(f"❌ Lỗi khi upload ảnh: {str(e)}")
                results[key] = None
        return results

@shared_task
def upload_files_to_cloudinary():
    """
    Upload files to Cloudinary and update file model
    """
    try:
        total = 0;
        with transaction.atomic():
            # Read file cloudinary_files.json
            with open('data/cloudinary/cloudinary_files.json', 'r', encoding='utf-8') as file:
                file_data_dict_result = json.load(file)

            # Upload files to Cloudinary and update file model
            for file_type, file_data in file_data_dict_result.items():
                if not file_data:
                    continue

                # Get folder and upload data
                folder = file_data['folder']
                upload_data = file_data['data']
                uploaded_images = upload_multiple_images(upload_data, folder)
                
                # If file type is SYSTEM, ABOUT_US, ICONS, only upload to Cloudinary and not update file model
                if file_type in ["SYSTEM", "ABOUT_US", "ICONS"]:
                    for key in uploaded_images.keys():
                        public_id = folder + key
                        logger.info(f"✅ {public_id} đã được upload")
                    continue
                
                # Upload files to Cloudinary and update file model
                for key, uploaded_json in uploaded_images.items():
                    public_id = folder + key
                    existing_file = File.objects.filter(public_id=public_id, file_type=file_type).first()
                    if not existing_file:
                        logger.error(f"❌ {public_id} không tồn tại")
                        continue
                    File.update_or_create_file_with_cloudinary(
                        file=existing_file,
                        cloudinary_upload_result=uploaded_json,
                        file_type=file_type
                    )
                    total += 1
                    logger.info(f"✅ {public_id} đã được upload")
        logger.info(f"✅ Upload files to Cloudinary và tạo file thành công: {total} file")
    except Exception as e:
        logger.error(f"❌ Upload files to Cloudinary và tạo file thất bại: {str(e)}")
        raise e
