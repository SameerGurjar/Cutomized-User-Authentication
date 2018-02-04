from django.conf.urls import url
from .views import UserRegisterAPIView, UserLoginAPIView


urlpatterns = [
		url(r'^register/$', UserRegisterAPIView.as_view(), name='register'),
		url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
]