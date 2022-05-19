from django.urls import include, path
from users.views import FollowApiView, FollowListAPIView

urlpatterns = [
    path('',
         include('djoser.urls')),
    path('auth/',
         include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/',
         FollowApiView.as_view(),
         name='subscribe'),
    path('users/subscriptions/',
         FollowListAPIView.as_view(),
         name='subscription'),
]
