from django.contrib import admin
from .models import Ingredient, Recipe, IngredientInRecipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'


class IngredientInRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInLine, )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    list_editable = ('name', 'color', 'slug',)
    search_fields = ('name', 'color',)
    list_filter = ('name', 'color', 'slug',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe)
