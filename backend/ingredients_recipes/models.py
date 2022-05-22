from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUserCreate


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единицы измерения')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_units')
        ]

    def __str__(self):
        return '{} - {}'.format(self.name, self.measurement_unit)


class Tag(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='Название')
    color = models.CharField(max_length=7,
                             unique=True,
                             verbose_name='Цвет в HEX')
    slug = models.SlugField(max_length=200,
                            unique=True,
                            verbose_name='Уникальный слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Список тегов')
    author = models.ForeignKey(CustomUserCreate,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientInRecipe',
                                         verbose_name='Список ингредиентов')
    name = models.CharField(max_length=200,
                            verbose_name='Название')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Ссылка на картинку на сайте')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        help_text='Время приготовления не может быть < 0',
        default=1,
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name} - {self.author}'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиенты')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепты')
    amount = models.PositiveSmallIntegerField(
        help_text='Количество не может быть < 0',
        default=1,
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ['-recipe']
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredient_in_recipe')
        ]
        verbose_name = 'Кол-во ингредиента в рецепте'
        verbose_name_plural = 'Кол-во ингредиентов в рецепте'

    def __str__(self):
        return '{} - {}'.format(self.recipe, self.ingredient)


class Favorite(models.Model):
    user = models.ForeignKey(CustomUserCreate,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='Рецепт')

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

        def __str__(self):
            return '{} добавил в избранное {}'.format(self.user, self.recipe)


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUserCreate,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_cart',
                               verbose_name='Рецепт')

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_cart'
            )
        ]
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
