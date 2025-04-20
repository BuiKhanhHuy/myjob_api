"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

from configs import variable_system as var_sys
from .models import (
    JobSeekerProfile,
    Resume
)


def save_profile(backend, user, response, *args, **kwargs):
    job_seeker_profile = JobSeekerProfile.objects.filter(user=user)
    if not job_seeker_profile.exists():
        job_seeker_profile = JobSeekerProfile.objects.create(user=user)
        Resume.objects.create(user=user,
                              job_seeker_profile=job_seeker_profile,
                              type=var_sys.CV_WEBSITE)
