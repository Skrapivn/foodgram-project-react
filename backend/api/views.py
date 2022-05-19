import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from ingredients_recipes.models import (Favorite, Ingredient,
                                        IngredientInRecipe, Recipe,
                                        ShoppingCart, Tag)

from .filters import IngredientFilter, RecipeFilter
from .pagination import PagePagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeWriteSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IngredientSerializer
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
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                Favorite, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = ShoppingCartSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            shopping_cart = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(detail=False, methods=('get',))
    def download_shopping_cart(self, request, *args, **kwargs):
        result = {}
        shopping_card = ShoppingCart.objects.filter(user=request.user)
        for i in shopping_card:
            ingredients = IngredientInRecipe.objects.filter(
                recipe=i.recipe
            )
            for i in ingredients:
                result.update({
                    i.ingredient.name:
                        [i.amount + result.get(i.ingredient.name, [0, ' '])[0],
                         i.ingredient.measurement_unit]
                })
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="cart.csv"'},
        )
        writer = csv.writer(response)
        for name, count in result.items():
            writer.writerow([name, str(count[0]), count[1]])
        return response
