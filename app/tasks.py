from users.models import User

def regular_balance_update(user_id: int, sum: int):
    try:
        user = User.objects.filter(id=user_id)
    except User.DoesNotExist:
        pass
    else:
        user.active_balance += sum
        user.save(update_fields=["active_balance"])

