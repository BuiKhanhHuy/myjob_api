"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from configs import variable_system as var_sys
from rest_framework import permissions


class IsJobSeekerUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return user.role_name == var_sys.JOB_SEEKER
        return False


class IsEmployerUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return user.role_name == var_sys.EMPLOYER
        return False


class ResumeOwnerPerms(IsJobSeekerUser):
    def has_object_permission(self, request, view, resume):
        return request.user == resume.user


class JobPostOwnerPerms(IsEmployerUser):
    def has_object_permission(self, request, view, job_post):
        return request.user == job_post.user


class CompanyImageOwnerPerms(IsEmployerUser):
    def has_object_permission(self, request, view, company_image):
        return request.user.company == company_image.company
