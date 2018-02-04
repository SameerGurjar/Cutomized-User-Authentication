from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomBackend(object):
    def authenticate(self, request, email=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            pass
        else:
            if self.user_can_authenticate(user):
                return user


    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None


    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except UserModel.DoesNotExist:
            return None



