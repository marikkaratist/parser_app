from django.urls import path
from .views import LogEntryCreateView

urlpatterns = [
    path('logs/', LogEntryCreateView.as_view())
]
