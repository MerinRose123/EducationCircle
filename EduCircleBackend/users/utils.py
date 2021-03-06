from users.models import User
from django.core.exceptions import ValidationError

def validate_user_based_on_uid(user_id):
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
        return user
    else:
        raise ValidationError("User not found", 400)