from django_filters import CharFilter
from django_filters.rest_framework import FilterSet, filters

from ingredients_recipes.models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ChoiceFilter(method='filter_author')
    is_favorited = filters.BooleanFilter(method='favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='shopping_cart_filter'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def author_filter(self, queryset, name, value):
        if value == 'me':
            return queryset.filter(author=self.request.user)
        return queryset.filter(author=value)

    def favorited_filter(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', method='istarts_with')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def istarts_with(self, queryset, slug, name):
        return queryset.filter(name__istartswith=name)
