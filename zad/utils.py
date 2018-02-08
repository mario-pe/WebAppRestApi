from django.contrib.auth.base_user import BaseUserManager


def serializer_sever(serializer):
    object = serializer.save()
    object.password = password_generator()
    object.save()


def password_generator():
    return BaseUserManager().make_random_password()
