from django_filters import CharFilter
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from ingredients_recipes.models import Recipe


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
        if value:  # !!!!!!!!!!!!!!and user.is_authenticated
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    CharFilter(field_name='name', lookup_expr='icontains')

# class RecipeFilter(FilterSet):
#     is_favorited = BooleanFilter(
#         method='filter_is_favorited'
#     )
#     is_in_shopping_cart = BooleanFilter(
#         method='filter_is_in_shopping_cart'
#     )
#     tags = ModelMultipleChoiceFilter(
#         field_name='tags__slug',
#         to_field_name='slug',
#         queryset=Tag.objects.all()
#     )
#     author = ChoiceFilter(
#         method='filter_author'
#     )

#     class Meta:
#         model = Recipe
#         fields = ('author', 'tags')

#     def filter_is_favorited(self, queryset, name, value):
#         user = self.request.user
#         if value == int(True) and user.is_authenticated:
#             return queryset.filter(favorites__user=user)
#         return queryset

#     def filter_is_in_shopping_cart(self, queryset, name, value):
#         user = self.request.user
#         if value == int(True) and user.is_authenticated:
#             return queryset.filter(shopping_cart__user=user)
#         return queryset

#     def filter_author(self, queryset, name, value):
#         if value == 'me':
#             return queryset.filter(author=self.request.user)
#         return queryset.filter(author=value)


# class IngredientFilter(SearchFilter):
#     search_param = 'name'
