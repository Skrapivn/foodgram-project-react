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
    # path('auth/', include('users.urls')),
    # path('', include('users.urls')),
]


# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from users.views import CustomUserViewSet
# from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet

# router = DefaultRouter()
# router.register('ingredients', IngredientViewSet, basename='ingredients')
# router.register('recipes', RecipeViewSet, basename='recipes')
# router.register('tags', TagViewSet, basename='tags')
# router.register('users', CustomUserViewSet, basename='users')


# urlpatterns = [
#     path('', include(router.urls)),
#     path('auth/', include('djoser.urls.authtoken')),
# ]
