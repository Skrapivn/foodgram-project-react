from django_filters import CharFilter
from django_filters.rest_framework import FilterSet, filters

from ingredients_recipes.models import (
    Favorite, Ingredient, Recipe, ShoppingCart,
)


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = CharFilter(field_name='author__id', lookup_expr='icontains')
    is_favorited = filters.BooleanFilter(method='favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='shopping_cart_filter'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def favorited_filter(self, queryset, name, value):
        favorite = Favorite.objects.filter(user=self.request.user.id)
        if value:
            return queryset.filter(favorites__in=favorite)
        return queryset.exclude(favorites__in=favorite)

    def shopping_cart_filter(self, queryset, name, value):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user.id)
        if value:
            return queryset.filter(shopping_cart__in=shopping_cart)
        return queryset.exclude(shopping_cart__in=shopping_cart)


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', method='istarts_with')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def istarts_with(self, queryset, slug, name):
        return queryset.filter(name__istartswith=name)
