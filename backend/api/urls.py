from django.urls import path
from .views import hello_world, spam_check

urlpatterns = [
    path('hello/', hello_world, name='hello'),
    path('check_spam/', spam_check, name='check_spam'),
]
