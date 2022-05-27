from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
