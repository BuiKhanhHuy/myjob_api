def get_current_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        current_user = request.user
    else:
        current_user = None

    return {'current_user': current_user}
