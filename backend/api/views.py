from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api import messages
from api.utils import get_download_shopping_cart
from ingredients_recipes.models import Ingredient, Recipe, ShoppingCart, Tag

from .filters import IngredientFilter, RecipeFilter
from .pagination import PagePagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          RecipeWriteSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = PagePagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = self.request.user.favorites.filter(recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(messages.UNFAVORITE_INFO,
                                status=status.HTTP_204_NO_CONTENT)
            return Response(
                messages.UNFAVORITE_ERROR,
                status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post', 'delete'],
            url_name='shopping_cart',
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = self.request.user.shopping_cart.filter(recipe=recipe)
        if request.method == 'POST':
            if shopping_cart.exists():
                return Response(
                    messages.CART_ADD_ERROR,
                    status=status.HTTP_400_BAD_REQUEST
                )

            shopping_cart = ShoppingCart.objects.create(
                user=self.request.user, recipe=recipe
            )
            shopping_cart.save()
            serializer = RecipeSerializer(recipe)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(
                    messages.CARD_DELETE_INFO,
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                messages.CARD_DELETE_ERROR,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(
        detail=False,
        url_name='download_shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        return get_download_shopping_cart(self, request)
