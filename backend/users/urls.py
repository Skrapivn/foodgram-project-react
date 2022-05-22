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




# from django.urls import include, path

# from djoser.views import TokenDestroyView
# from rest_framework.routers import DefaultRouter

# from .views import TokenCreateView, UserViewSet

# router_v1 = DefaultRouter()

# router_v1.register('', UserViewSet, basename='users')

# token = [
#     path('login/', TokenCreateView.as_view(), name='login'),
#     path('logout/', TokenDestroyView.as_view(), name='logout'),
# ]


# urlpatterns = [
#     path('', include(router_v1.urls)),
#     path('token/', include(token)),
# ]
