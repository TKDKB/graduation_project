from django.core.handlers.wsgi import WSGIRequest


def regular_balance_update(request:WSGIRequest, sum: int):
    request.user.active_balance += sum
    request.user.save()
