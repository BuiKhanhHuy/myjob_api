from .models import User


def create_user(strategy, backend, user=None, *args, **kwargs):
    print(kwargs)
    if user:
        return {'is_new': False}

    full_name = kwargs.get('response').get('name')
    email = kwargs.get('response').get('email')

    if not email:
        raise Exception('Email is required for registration')

    user = User.objects.create_user(
        email=email,
        full_name=full_name
    )

    return {'is_new': True, 'user': user}

