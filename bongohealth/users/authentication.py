from django.contrib.auth.models import User

class EmailBackendAuth():
    """Authenticate using an email backend"""
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except(User.MultipleObjectsReturned, User.DoesNotExist):
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
