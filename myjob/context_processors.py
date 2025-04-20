"""
MyJob Recruitment System - Part of MyJob Platform

Author: Bui Khanh Huy
Email: khuy220@gmail.com
Copyright (c) 2023 Bui Khanh Huy

License: MIT License
See the LICENSE file in the project root for full license information.
"""

def get_current_user(request):
    if request.user.is_authenticated and request.user.is_staff:
        current_user = request.user
    else:
        current_user = None

    return {'current_user': current_user}
