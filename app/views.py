from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.decorators import login_required

