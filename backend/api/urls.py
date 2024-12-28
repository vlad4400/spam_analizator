from django.urls import path
from .views import spam_check

urlpatterns = [
    path('check_spam/', spam_check, name='check_spam'),
]
