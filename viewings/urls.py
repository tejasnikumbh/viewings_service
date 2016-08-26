from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^viewings/$', views.Viewings.as_view(), name="viewings"),
	url(r'^conversations/$', views.Conversations.as_view(), name="conversations")
]