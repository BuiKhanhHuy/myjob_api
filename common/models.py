"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from django.db import models
from django.conf import settings


class CommonBaseModel(models.Model):
    class Meta:
        abstract = True

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class City(CommonBaseModel):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "myjob_common_city"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class District(CommonBaseModel):
    name = models.CharField(max_length=50)

    # ForeignKey
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name="districts")

    class Meta:
        db_table = "myjob_common_district"

    def __str__(self):
        return self.name


class Location(CommonBaseModel):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True,
                             related_name="locations")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True,
                                 related_name="locations")
    address = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "myjob_common_location"

    def __str__(self):
        return f"City: {self.city.name if self.city else '---'} / District: {self.district.name if self.district else '---'} / Address: {self.address} / Location: ({self.lat}:{self.lng})"


class Career(CommonBaseModel):
    name = models.CharField(max_length=150)
    app_icon_name = models.CharField(max_length=50, null=True)
    icon = models.OneToOneField("File", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "myjob_common_career"

    def __str__(self):
        return self.name


class File(CommonBaseModel):
    AVATAR_TYPE = 'AVATAR'
    CV_TYPE = 'CV'
    LOGO_TYPE = 'LOGO'
    COVER_IMAGE_TYPE = 'COVER_IMAGE'
    COMPANY_IMAGE_TYPE = 'COMPANY_IMAGE'
    CAREER_IMAGE_TYPE = 'CAREER_IMAGE'
    WEB_BANNER_TYPE = 'WEB_BANNER'
    MOBILE_BANNER_TYPE = 'MOBILE_BANNER'
    SYSTEM_TYPE = 'SYSTEM'
    OTHER_TYPE = 'OTHER'
    FILE_TYPES = [
        (AVATAR_TYPE, 'Avatar'),
        (CV_TYPE, 'CV'),
        (LOGO_TYPE, 'Logo'),
        (COVER_IMAGE_TYPE, 'Cover Image'),
        (COMPANY_IMAGE_TYPE, 'Company Image'),
        (CAREER_IMAGE_TYPE, 'Career Image'),
        (WEB_BANNER_TYPE, 'Web Banner'),
        (MOBILE_BANNER_TYPE, 'Mobile Banner'),
        (SYSTEM_TYPE, 'System'),
        (OTHER_TYPE, 'Other')
    ]
    
    RESOURCE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('raw', 'Raw File'),
    ]

    public_id = models.CharField(max_length=255)
    version = models.CharField(max_length=20, null=True, blank=True)
    format = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    file_type = models.CharField(max_length=50, choices=FILE_TYPES, default=OTHER_TYPE)
    uploaded_at = models.DateTimeField(null=False, blank=False)
    metadata = models.JSONField(blank=True, null=True)
    
    def get_full_url(self):
        from helpers.cloudinary_service import CloudinaryService
        url, _ = CloudinaryService.get_url_from_public_id(self.public_id, {
            'version': self.version,
            'format': self.format,
            'resource_type': self.resource_type,
        })
        return url
    
    @staticmethod
    def update_or_create_file_with_cloudinary(file, cloudinary_upload_result, file_type: str = OTHER_TYPE):
        file_data = {
            "public_id": cloudinary_upload_result.get("public_id"),
            "version": cloudinary_upload_result.get("version"),
            "format": cloudinary_upload_result.get("format"),
            "resource_type": cloudinary_upload_result.get("resource_type"),
            "uploaded_at": cloudinary_upload_result.get("created_at"),
            "metadata": cloudinary_upload_result,
            "file_type": file_type
        }
        if file:
            # Update file
            for key, value in file_data.items():
                setattr(file, key, value)
            file.save()
        else:
            # Create file
            file = File.objects.create(**file_data)
        return file
    
    class Meta:
        db_table = "myjob_files"
        ordering = ['-create_at']