from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('auth/', include('users.urls')),
    path('', include('users.urls')),
]


# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

# router = DefaultRouter()
# router.register('ingredients', IngredientsViewSet, basename='ingredients')
# router.register('tags', TagsViewSet, basename='tags')
# router.register('recipes', RecipeViewSet, basename='recipes')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# ____________________________________________


# from django.urls import include, path

# from rest_framework.routers import DefaultRouter

# from .views import IngredientViewSet, RecipeViewSet, TagViewSet

# router_v1 = DefaultRouter()

# router_v1.register('tags', TagViewSet, basename='tags')
# router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
# router_v1.register('recipes', RecipeViewSet, basename='recipes')

# urlpatterns = [
#     path('', include(router_v1.urls)),
#     path('auth/', include('users.urls')),
#     path('users/', include('users.urls')),
# ]
